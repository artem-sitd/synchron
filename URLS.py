from config import ClientID
from urllib.parse import quote
import config

# В каждый запрос в headers необходимо вставлять
head_auth = {'Authorization': f'OAuth {config.OAuth_TOKEN}'}

# URL для первичного получения токена
get_OAuth_TOKEN = f'https://oauth.yandex.ru/authorize?response_type=token&client_id={ClientID}'

# URL для проверки токена
check_token_url = "https://cloud-api.yandex.net/v1/disk/"


# URL для проверки папки, удаления и  записи файлов в облаке
def upload_get_delete_urls(folder, upload='', overwrite=''):
    return f'https://cloud-api.yandex.net/v1/disk/resources{upload}?path=disk:/{quote(folder)}{str(overwrite).lower()}'


# URL для получения информации о диске

