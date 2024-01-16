"""
Чтобы обеспечить дальнейшее расширение программы для работы с другими файловыми сервисами, логика работы
с конкретным облачным хранилищем должна быть вынесена в отдельный класс и файл. Конструктор этого класса должен
принимать токен доступа и путь к существующей папке для хранения резервных копий в удалённом хранилище.
Этот класс должен предоставлять методы:

○	load(path) — для загрузки файла в хранилище;
○	reload(path) — для перезаписи файла в хранилище;
○	delete(filename) — для удаления файла из хранилища;
○	get_info() — для получения информации о хранящихся в удалённом хранилище файлах.
"""


class YandexCloud:
    def __init__(self, oauth_token=None, local_path=None, cloud_path=None):
        self.oauth_token = oauth_token
        self.local_path = local_path
        self.cloud_path = cloud_path

    def load(self):
        pass

    def reload(self):
        pass

    def delete(self, filename):
        pass

    def get_info(self):
        pass
