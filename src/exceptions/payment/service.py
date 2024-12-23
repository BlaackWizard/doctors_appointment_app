from fastapi import HTTPException, status

from src.exceptions.base import ApplicationException


class NotFoundServiceException(ApplicationException):
    @property
    def message(self):
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Не удалось найти услугу по такому ID',
        )


class CreateServiceCanOnlyAdminException(ApplicationException):
    @property
    def message(self):
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Услуги могут создавать только администраторы',
        )
