import hashlib
import config
import os.path
import json


# Расчет кэша для локальных файлов
def calculate_file_hash(file_path):
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as file:
        while chunk := file.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()


# Сравнение хэшей старых и новых
def hash_compare(new_hash: dict):
    old_hash = os.path.exists(os.path.join(config.SELF_FOLDER, 'old_hash.json'))
    added_by_hash = set()
    if old_hash:
        with open(os.path.join(config.SELF_FOLDER, 'old_hash.json'), 'r') as old:
            old_hash = json.load(old)
            for k, v in new_hash.items():
                if k in old_hash and v != old_hash[k]:
                    added_by_hash.add(k)
        return added_by_hash
    return new_hash


def create_hash():
    actual_hash = os.path.join(config.SELF_FOLDER, 'actual_hash.json')
    old_hash = os.path.join(config.SELF_FOLDER, 'old_hash.json')
    # Проверка наличия файла 'old_hash.json'
    if os.path.exists(old_hash):
        # Удаляем существующий файл 'old_hash.json'
        os.remove(old_hash)

    # Переименовываем 'actual_hash.json' в 'old_hash.json'
    os.rename(actual_hash, old_hash)
