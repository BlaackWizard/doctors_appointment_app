from src.exceptions.base import ApplicationException


class NotFoundUserException(ApplicationException):
    @property
    def message(self):
        return 'Не удалось найти пользователя'


class NotFoundUserExceptionOrIncorrectPassword(ApplicationException):
    @property
    def message(self):
        return 'Неправильный логин или пароль, проверьте имя пользователя и пароль'
