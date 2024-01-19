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
from URLS import head_auth, upload_get_delete_urls
import config
import requests
from hashwork import calculate_file_hash, hash_compare, create_hash


class YandexCloud:
    def __init__(self, oauth_token=None, local_path=None, cloud_path=None):
        self.oauth_token = oauth_token
        self.local_path = local_path
        self.cloud_path = cloud_path

    # Добавить проверку на существование папки. Может удалил или перейменовал
    # Получение списка файлов локальной папки
    def list_local_files(self):
        dict_hash_local = {f: calculate_file_hash(os.path.join(self.local_path, f)) for f in os.listdir(self.local_path)
                           if
                           os.path.isfile(os.path.join(self.local_path, f))}
        if dict_hash_local:
            with open('actual_hash.json', 'w') as file:
                print(dict_hash_local, file=file)
            return dict_hash_local
        else:
            print('Произошла ошибка в блоке list_local_files')
            return False

    # Добавить проверку на существование папки. Может удалил или перейменовал
    # Полученеи списка файлов облака
    def list_yandex_disk_files(self):
        response = requests.get(upload_get_delete_urls(self.cloud_path), headers=head_auth)
        if response.status_code == 200:
            return [item["name"] for item in response.json().get("_embedded", {}).get("items", [])]
        return False

    # Сравнение содержимого облака и локальной папки
    def compare_lists(self, local_files, cloud_files):
        delete = set(cloud_files) - set(local_files.keys())
        added_by_name = set(local_files.keys()) - set(
            cloud_files)  # Имена файлов, которых нет в облаке. Предварительный список
        return added_by_name, delete

    # Загрузка/перезапись файлов в облаке
    def load(self, files_to_upload):
        for file in files_to_upload:
            # Получение URL для загрузки
            url = upload_get_delete_urls(file, upload='/upload', overwrite=True)
            response = requests.get(url, headers=head_auth)
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

    def reload(self):
        # этот метод не исопльзую, но в тз он нужен
        pass

    # Удаление файлов в облаке
    def delete(self, deleted_files):
        for file in deleted_files:
            url = upload_get_delete_urls(f'{self.cloud_path}/{file}')
            response = requests.delete(url, headers=head_auth)
            if response.status_code != 204:
                print(f"Failed to delete {file}. Status code: {response.status_code}, Response: {response.text}")
            else:
                print(f'Файл {file} удален из облака')

    # Получение инфо о папке в облаке
    def get_info(self):
        # пока не делал, можно использовать URL для проверки токена
        pass

    # Запуск синхронизации
    def update(self):
        dict_hash_local = self.list_local_files()  # Словарь хэшей файлов в локальной папке
        cloud_files = self.list_yandex_disk_files()  # список файлов в папке облака

        # added_files -Добавленные файлы, которых нет в облаке
        # deleted_files - удаленные файлы из локального хранилища, но которые еще есть в облаке
        added_by_name, deleted_files = self.compare_lists(dict_hash_local, cloud_files)
        if deleted_files:
            self.delete(deleted_files)
        if added_by_name:
            for name in added_by_name:
                del dict_hash_local[name]
        added_by_hash = hash_compare(dict_hash_local)
        files_to_upload = added_by_hash | added_by_name
        self.load(files_to_upload)
        # переименовываем файлы хэшей
        create_hash()
        print('Синхронизация произведена')
