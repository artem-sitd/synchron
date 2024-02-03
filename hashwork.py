import hashlib
import json
import os.path

import config


# Расчет кэша для локальных файлов
def calculate_file_hash(file_path):
    hasher = hashlib.sha256()
    with open(file_path, "rb") as file:
        while chunk := file.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()


# Сравнение хэшей старых и новых
def hash_compare(new_hash: dict):
    parent_folder = os.path.dirname(os.path.abspath(__file__))
    old_hash_exists = os.path.exists(os.path.join(parent_folder, "old_hash.json"))
    path_old_hash = os.path.join(parent_folder, "old_hash.json")
    added_by_hash = set()
    if old_hash_exists:
        with open(path_old_hash, "r") as old:
            old_hash = json.load(old)
            for k, v in new_hash.items():
                value_old_hash = old_hash.get(k)
                if value_old_hash and value_old_hash != v:
                    added_by_hash.add(k)
        return added_by_hash
    return set(new_hash)


# Создание json, хранящих хэши
def create_hash():
    parent_folder = os.path.dirname(config.SELF_FOLDER)
    actual_hash = os.path.join(parent_folder, "actual_hash.json").replace("\\", "/")
    old_hash = os.path.join(parent_folder, "old_hash.json").replace("\\", "/")
    # Проверка наличия файла 'old_hash.json'
    if os.path.exists(old_hash):
        # Удаляем существующий файл 'old_hash.json'
        print("обнаружен старый хэш, удаляем")
        os.remove(old_hash)
    if os.path.exists(actual_hash):
        print("переименовываем хэш")
        # Переименовываем 'actual_hash.json' в 'old_hash.json'
        os.rename(actual_hash, old_hash)
    else:
        print("actual_hash.json не обнаружен!")
