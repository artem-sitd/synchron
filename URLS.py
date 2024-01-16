from config import ClientID
from urllib.parse import quote
import config

# В каждый запрос в headers необходимо вставлять
head_auth = {'Authorization': f'OAuth {config.OAuth_TOKEN}'}

# URL для проверки токена
check_token_url = "https://cloud-api.yandex.net/v1/disk/"


# URL для проверки cloud_folder
def cloud_folder_url(folder):
    return f"https://cloud-api.yandex.net/v1/disk/resources?path=disk:/{quote(folder)}"


# URL для первичного получения токена
get_OAuth_TOKEN = f'https://oauth.yandex.ru/authorize?response_type=token&client_id={ClientID}'

# URL для записи

# URL для получения информации о диске

# URL для удаления

# URL для перезаписи
