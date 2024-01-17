import requests

# Параметры запроса для получения URL для загрузки файла
disk_path = '/folder/file.txt'
overwrite = True
get_upload_url_url = f'https://cloud-api.yandex.net/v1/disk/resources/upload?path={disk_path}&overwrite=true'

# Ваш OAuth-токен
oauth_token = 'ваш_токен'

# Получение URL для загрузки
response = requests.get(get_upload_url_url, headers={'Authorization': f'OAuth {oauth_token}'})

if response.status_code == 200:
    # Извлекаем URL для загрузки из ответа
    upload_url = response.json()['href']

    # Путь к локальному файлу
    local_file_path = '/path/to/local/file.txt'

    # Загрузка файла на полученный URL
    with open(local_file_path, 'rb') as file:
        upload_response = requests.put(upload_url, files={'file': file})

    if upload_response.status_code == 201:
        print("File uploaded successfully.")
    else:
        print(f"Failed to upload file. Status code: {upload_response.status_code}, Response: {upload_response.text}")
else:
    print(f"Failed to get upload URL. Status code: {response.status_code}, Response: {response.text}")
