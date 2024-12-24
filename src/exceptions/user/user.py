from fastapi import HTTPException, status

from src.exceptions.base import ApplicationException


class MultipleResultsFoundException(ApplicationException):
    @property
    def message(self):
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Найдено несколько записей с таким именем, введите конкретнее'
        )