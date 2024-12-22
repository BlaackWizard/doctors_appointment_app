from fastapi import HTTPException, status

from src.exceptions.base import ApplicationException


class NotFoundAppointmentException(ApplicationException):
    @property
    def message(self):
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Не удалось найти запись по этому ID. Проверьте еще раз ID записи',
        )


class AppointmentAlreadyExistsException(ApplicationException):
    @property
    def message(self):
        return HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail='У вас уже запланирована эта запись',
        )
