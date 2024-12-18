from src.exceptions.base import ApplicationException


class UserAlreadyExistsException(ApplicationException):
    @property
    def message(self):
        return 'Пользователь с данным именем уже существует'
