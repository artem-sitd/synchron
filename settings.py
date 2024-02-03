import os.path
import time
from shlex import quote

import requests

import config
import messages as MS
from URLS import upload_get_delete_urls, get_headers, check_token_url, check_available_url
from config import start_env
# Настройка папки в облаке
from yandex import YandexCloud


# настройка удаленной папки
def set_cloud_folder(user1):
    for _ in MS.set_CLOUD_FOLDER:
        print(_)
    headers = get_headers(user1.oauth_token)
    # проверка соединения с интернетом
    if check_available_url(check_token_url, headers=headers):
        while True:
            cloud_folder = input()
            try:
                response = requests.get(upload_get_delete_urls(cloud_folder), headers=headers)
                if response.status_code == 200:
                    with open('.env', 'a') as data:
                        print(f'\nCLOUD_FOLDER="{cloud_folder}"', file=data)
                    print('Папка зарегистрирована. Все настройик выполнены - начинаем работу.\n')
                    setattr(user1, 'cloud_path', cloud_folder)
                    break
                else:
                    for _ in MS.wrong_cloud_folder:
                        print(_)
            except Exception as er:
                print('что-то пошло не так в set_cloud_folder', 'ошибка:', er)
        # запуск процедуры обновления
        start_env()
        # while True:
        user1.update()
    else:
        print('сервис недоступен Проверьте соединение с интернетом')
        with open('.env', 'w') as file:
            pass
        choice_to_start()


# Настройка периода обновления
def set_period(user1):
    for _ in MS.set_PERIOD:
        print(_)
    while True:
        try:
            period = int(input())
            with open('.env', 'a') as data:
                print(f'\nPERIOD="{period}"', file=data)
            setattr(user1, 'period', period)
            print('Задан период: ', period, 'секунд')
            break
        except ValueError:
            print('Необходимо вводить только цифры. Введите период '
                  'обновления в секундах: ')
    set_cloud_folder(user1)


# Настройке отслеживаемой локальной папки
def set_self_folder(user1):
    for _ in MS.set_SELF_FOLDER:
        print(_)
    while True:
        path_to_local_folder = os.path.abspath(input()).replace('\\', '/')
        print(path_to_local_folder)
        if os.path.exists(path_to_local_folder):
            with open('.env', 'a') as data:
                print(f'\nSELF_FOLDER="{path_to_local_folder}"', file=data)
            setattr(user1, 'local_path', path_to_local_folder)
            print('Локальная папка установлена\n')
            break
        else:
            print('По указанному пути указанной папки не обнаружено, укажите путь '
                  'к локальной папке: ')
    set_period(user1)


# Проверка корректности токена
def check_token(token) -> bool:
    headers = get_headers(token)
    # проверка соединения с интернетом
    if check_available_url(check_token_url, headers=headers):
        try:
            response_check_token = requests.get(check_token_url, headers=headers)
            if response_check_token.status_code == 200:
                print('Токен актуален и корректен\n')
                return True
            else:
                return False
        except Exception as er:
            print('что-то пошло не так в check_token', 'ошибка:', er)
            return False
    else:
        print('сервис недоступен Проверьте соединение с интернетом')
        with open('.env', 'w') as file:
            pass
        choice_to_start()


# Настройка токена
def set_token(user1):
    for _ in MS.greetings_new(user1.clientid):
        print(_)
    oauth_token = input()
    if check_token(oauth_token):
        with open('.env', 'a') as data:
            print(f'\nOAuth_TOKEN="{oauth_token}"', file=data)
        setattr(user1, 'oauth_token', oauth_token)
        set_self_folder(user1)
    else:
        print('>>> Предоставленный токен или clientID не верен, начнем еще '
              'раз заново\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        # очищаем .env, начинаем все заново
        with open('.env', 'w') as data:
            pass
        set_client_id()


# настройка clientID
def set_client_id(user1=None):
    for _ in MS.set_CLIENTID:
        print(_)
    clientid = input()
    with open('.env', 'a') as data:
        print(f'ClientID="{clientid}"', file=data)
    user1 = YandexCloud(clientid=clientid)
    set_token(user1)


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
                print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
                print('Принято', choice_to_work)
                break
        except ValueError:
            print('Необходимо вводить только цифры')
    if choice_to_work == 1:
        print('Приступаем к настройкам\n')
        set_client_id()
    if choice_to_work == 2:
        start_env()
        # while True:
        user1 = YandexCloud(clientid=config.ClientID, oauth_token=config.OAuth_TOKEN,
                            local_path=config.SELF_FOLDER, cloud_path=config.CLOUD_FOLDER, period=config.PERIOD)
        while True:
            print('\nНачинаем работу\n')
            user1.update()
            time.sleep(config.PERIOD)
