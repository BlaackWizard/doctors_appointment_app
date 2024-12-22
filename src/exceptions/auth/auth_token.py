from fastapi import HTTPException, status

from src.exceptions.base import ApplicationException


class TokenExpiredException(ApplicationException):
    @property
    def message(self):
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Срок действия токена истёк")


class TokenIsNotValidException(ApplicationException):
    @property
    def message(self):
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен не валидный")


class NotFoundTokenException(ApplicationException):
    @property
    def message(self):
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен не найден")
