import os
from dotenv import load_dotenv, find_dotenv

OAuth_TOKEN, ClientID, SELF_FOLDER, CLOUD_FOLDER, PERIOD = None, None, None, None, None


def start_env():
    global OAuth_TOKEN, ClientID, SELF_FOLDER, CLOUD_FOLDER, PERIOD
    print('Загружаем переменные .env')
    if not find_dotenv():
        exit("Переменные окружения не загружены т.к отсутствует файл .env")
    else:
        load_dotenv()
        OAuth_TOKEN = os.getenv('OAuth_TOKEN')
        ClientID = os.getenv('ClientID')
        SELF_FOLDER = os.getenv('SELF_FOLDER')
        CLOUD_FOLDER = os.getenv('CLOUD_FOLDER')
        PERIOD = os.getenv('PERIOD')
