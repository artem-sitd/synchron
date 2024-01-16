import requests
import json
from urllib.parse import quote
import config

token = config.OAuth_TOKEN

folder_name = "социальные сети"

encoded_folder_name = quote(folder_name)

url3 = f"https://cloud-api.yandex.net/v1/disk/resources?path=disk:/{encoded_folder_name}"

def cloud_folder_url(folder):
    return (f"https://cloud-api.yandex.net/v1/disk/resources?path={folder}")

check_token_url = "https://cloud-api.yandex.net/v1/disk/"

response1 = requests.get(url3, headers={'Authorization': f'OAuth {token}'})

response2 = requests.get(check_token_url, headers={'Authorization': f'OAuth {token}'})

response3 = requests.get("https://cloud-api.yandex.net/v1/disk/resources/files?path=%2FЗагрузки%2F",
                         headers={'Authorization': f'OAuth {token}'})

print(response1.status_code)
print(response1)
