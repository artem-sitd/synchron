"""
Чтобы обеспечить дальнейшее расширение программы для работы с другими файловыми сервисами, логика работы
с конкретным облачным хранилищем должна быть вынесена в отдельный класс и файл. Конструктор этого класса должен
принимать токен доступа и путь к существующей папке для хранения резервных копий в удалённом хранилище.
Этот класс должен предоставлять методы:

○	load(path) — для загрузки файла в хранилище;
○	reload(path) — для перезаписи файла в хранилище;
○	delete(filename) — для удаления файла из хранилища;
○	get_info() — для получения информации о хранящихся в удалённом хранилище файлах.
"""
import os
import json
from URLS import get_headers, upload_get_delete_urls, check_available_url, check_token_url
import config
import requests
from hashwork import calculate_file_hash, hash_compare, create_hash


class YandexCloud:
    def __init__(self, clientid=None, oauth_token=None, local_path=None, cloud_path=None, period=None):
        self.clientid = clientid
        self.oauth_token = oauth_token
        self.local_path = local_path
        self.cloud_path = cloud_path
        self.period = period

    def __str__(self):
        return f'clientid= {self.clientid}, token= {self.oauth_token}, ' \
               f'local_path= {self.local_path}, cloud_path= {self.cloud_path}, period={self.period}'

    # Добавить проверку на существование папки. Может удалил или перейменовал
    # Получение списка файлов локальной папки
    def list_local_files(self):
        print('заходим в list_local_files')
        print(config.SELF_FOLDER)
        dict_hash_local = {}
        for file in os.listdir(config.SELF_FOLDER):
            if os.path.isfile(os.path.join(config.SELF_FOLDER, file)):
                dict_hash_local[file] = calculate_file_hash(os.path.join(config.SELF_FOLDER, file))
        if dict_hash_local:
            with open('actual_hash.json', 'w') as file:
                json.dump(dict_hash_local, file)
            return dict_hash_local
        else:
            print('Произошла ошибка в блоке list_local_files')
            return False

    # Полученеи списка файлов облака
    def list_yandex_disk_files(self):
        headers = get_headers(self.oauth_token)
        # проверка соединения с интернетом
        if check_available_url(check_token_url, headers=headers):
            response = requests.get(upload_get_delete_urls(config.CLOUD_FOLDER),
                                    headers=headers)
            if response.json()['name'] == config.CLOUD_FOLDER:
                if response.status_code == 200:
                    return [item["name"] for item in response.json().get("_embedded", {}).get("items", [])]
                print(f'list_yandex_disk_files:, code: {response.status_code},response: {response.text}')
                return None
            else:
                print('Папка в облаке отсутсвует по указанному пути')
                return None
        else:
            print('сервис недоступен Проверьте соединение с интернетом')
            exit(1)

    # Сравнение содержимого облака и локальной папки
    def compare_lists(self, local_files, cloud_files):
        delete = set(cloud_files) - set(local_files.keys())
        added_by_name = set(local_files.keys()) - set(
            cloud_files)  # Имена файлов, которых нет в облаке. Предварительный список
        return added_by_name, delete

    # Загрузка/перезапись файлов в облаке
    def load(self, files_to_upload):
        headers = get_headers(self.oauth_token)
        # проверка соединения с интернетом
        if check_available_url(check_token_url, headers=headers):
            for file in files_to_upload:
                # Получение URL для загрузки
                url = upload_get_delete_urls(f'{config.CLOUD_FOLDER}/{file}', upload='/upload',
                                             overwrite='&overwrite=true')
                response = requests.get(url, headers=headers)

                if response.status_code == 200:
                    # Извлекаем URL для загрузки из ответа
                    upload_url = response.json()['href']

                    # Путь к локальному файлу
                    local_file_path = os.path.join(config.SELF_FOLDER, file)

                    # Загрузка файла на полученный URL
                    with open(local_file_path, 'rb') as f:
                        upload_response = requests.put(upload_url, files={'file': f})

                    if upload_response.status_code == 201:
                        print(f'Файл: {file} загружен в облако')
                    else:
                        print(
                            f"Failed to upload file. Status code: {upload_response.status_code}, Response: {upload_response.text}")
                else:
                    print(f"Failed to get upload URL. Status code: {response.status_code}, Response: {response.text}")
        else:
            print('сервис недоступен Проверьте соединение с интернетом')
            exit(1)

    # Удаление файлов в облаке
    def delete(self, deleted_files):
        headers = get_headers(self.oauth_token)
        # проверка соединения с интернетом
        if check_available_url(check_token_url, headers=headers):
            for file in deleted_files:
                url = upload_get_delete_urls(f'{config.CLOUD_FOLDER}/{file}')
                response = requests.delete(url, headers=headers)
                if response.status_code != 204:
                    print(f"Failed to delete {file}. Status code: {response.status_code}, Response: {response.text}")
                else:
                    print(f'Файл {file} удален из облака')
        else:
            print('сервис недоступен Проверьте соединение с интернетом')
            exit(1)

    # Получение инфо о папке в облаке
    def get_info(self):
        # пока не делал, можно использовать URL для проверки токена
        pass

    # Запуск синхронизации
    def update(self):
        print('Получаем перечень локальных файлов')
        dict_hash_local = self.list_local_files()  # Словарь хэшей файлов в локальной папке
        print('Получаем перечень файлов в облаке')
        cloud_files = self.list_yandex_disk_files()  # список файлов в папке облака
        print('cloud_files:', cloud_files)
        added_by_name, deleted_files = self.compare_lists(dict_hash_local, cloud_files)
        if deleted_files:
            self.delete(deleted_files)
        if added_by_name:
            for name in added_by_name:
                del dict_hash_local[name]
        added_by_hash = hash_compare(dict_hash_local)
        print('added_by_hash:', added_by_hash)
        print('added_by_name:', added_by_name)
        print('deleted_files:', deleted_files)
        files_to_upload = added_by_hash | added_by_name
        print('files_to_upload', files_to_upload)
        self.load(files_to_upload)

        # переименовываем файлы хэшей
        create_hash()
        print('Синхронизация произведена, программа в режиме ожидания на ', config.PERIOD, 'секунд')
        return
