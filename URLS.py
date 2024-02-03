from urllib.parse import quote

import requests


# В каждый запрос к api в headers необходимо вставлять
def get_headers(token=None):
    headers = {"Authorization": f"OAuth {token}"}
    return headers


# URL для первичного получения токена
def get_token_url(clientid=None):
    url = f"https://oauth.yandex.ru/authorize?response_type=token&client_id={clientid}"
    return url


# URL для проверки токена
check_token_url = "https://cloud-api.yandex.net/v1/disk/"


# URL для проверки папки, удаления и  записи файлов в облаке
def upload_get_delete_urls(folder, upload="", overwrite=""):
    url = f"https://cloud-api.yandex.net/v1/disk/resources{upload}?path=disk:/{quote(folder)}{overwrite}"
    return url


def check_available_url(url, timeout=10, headers=None):
    try:
        response = requests.get(url, timeout=timeout, headers=headers)
        response.raise_for_status()
        return True  # URL доступен
    except requests.exceptions.Timeout:
        print(f"check_available_url, Превышено время ожидания при обращении к {url}")
        return False  # Превышено время ожидания
    except requests.exceptions.RequestException as e:
        print(f"check_available_url, Ошибка при обращении к {url}: {e}")
        return False  # Другая ошибка при обращении
