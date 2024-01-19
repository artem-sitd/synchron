import os.path
import requests
import config
import messages as MS
from URLS import upload_get_delete_urls, head_auth, check_token_url

# Настройка папки в облаке
from yandex import YandexCloud


def set_cloud_folder():
    for _ in MS.set_CLOUD_FOLDER:
        print(_)
    while True:
        cloud_folder = input()
        try:
            response = requests.get(upload_get_delete_urls(cloud_folder), headers=head_auth)
            if response.status_code == 200:
                with open('.env', 'a') as data:
                    print(f'\nCLOUD_FOLDER="{cloud_folder}"', file=data)
                print('Папка зарегистрирована. Все настройик выполнены - начинаем работу.\n')
                user1 = YandexCloud(oauth_token=config.OAuth_TOKEN, local_path=config.SELF_FOLDER,
                                    cloud_path=config.CLOUD_FOLDER)
                user1.update()
            else:
                for _ in MS.wrong_cloud_folder:
                    print(_)
        except Exception as er:
            print('что-то пошло не так', 'ошибка:', er)


# Настройка периода обновления
def set_period():
    for _ in MS.set_PERIOD:
        print(_)
    while True:
        try:
            period = int(input())
            with open('.env', 'a') as data:
                print(f'\nPERIOD="{period}"', file=data)
            print('Задан период: ', period, 'секунд')
            break
        except ValueError:
            print('Необходимо вводить только цифры. Введите период обновления в секундах: ')
    set_cloud_folder()


# Настройке отслеживаемой локальной папки
def set_self_folder():
    for _ in MS.set_SELF_FOLDER:
        print(_)
    while True:
        path = input()
        if os.path.exists(path):
            with open('.env', 'a') as data:
                print(f'\nSELF_FOLDER="{path}"', file=data)
            print('Локальная папка установлена\n')
            break
        else:
            print('По указанному пути указанной папки не обнаружено, укажите путь к локальной папке: ')
    set_period()


# Проверка корректности токена
def check_token() -> bool:
    try:
        response_check_token = requests.get(check_token_url, headers=head_auth)
        if response_check_token.status_code == 200:
            print('Токен актуален и корректен\n')
            return True
    except Exception as er:
        print('что-то пошло не так', 'ошибка:', er)
        return False


# Настройка токена
def set_token():
    for _ in MS.greetings_new:
        print(_)
    while True:
        token = input()
        if check_token():
            with open('.env', 'a') as data:
                print(f'\nOAuth_TOKEN="{token}"', file=data)
                break
        else:
            print('Попробуем еще раз. Введите токен: ')
    set_self_folder()


# Выбор способа работы. С настройкой или без
def choice_to_start():
    for _ in MS.choice_to_work:
        print(_)
    while True:
        try:
            choice_to_work = int(input())
            if choice_to_work not in range(1, 3):
                print('Введите 1 или 2')
            else:
                print('Принято', choice_to_work)
                break
        except ValueError:
            print('Необходимо вводить только цифры')
    if choice_to_work == 1:
        print('\nПриступаем к настройкам\n')
        set_token()
    if choice_to_work == 2:
        # вставить исполняемую функцию
        print('\nНачинаем работу\n')
