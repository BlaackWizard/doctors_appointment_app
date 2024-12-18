from fastapi import HTTPException, status

from src.exceptions.base import ApplicationException


class NotFoundUserException(ApplicationException):
    @property
    def message(self):
        return HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Пользователь не найден')


class NotFoundUserExceptionOrIncorrectPassword(ApplicationException):
    @property
    def message(self):
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Неправильный логин или пароль, проверьте имя пользователя и пароль',
        )


class NotFoundUserByIDException(ApplicationException):
    @property
    def message(self):
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Не найден врач по этому id')


class UserAlreadyExistsException(ApplicationException):
    @property
    def message(self):
        return HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Пользователь с данным именем уже существует')


class UserNotFoundOrUserIsNotDoctorException(ApplicationException):
    @property
    def message(self):
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не найден в базе данных или пользователь не является доктором",
        )
