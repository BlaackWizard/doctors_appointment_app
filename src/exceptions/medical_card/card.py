from fastapi import HTTPException, status

from src.exceptions.base import ApplicationException


class NotFoundMedicalCardException(ApplicationException):
    @property
    def message(self):
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Не удалось найти мед.карту в базе данных")


class ThisIsNotYourMedicalCardException(ApplicationException):
    @property
    def message(self):
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Это не ваша медицинская карта!")
