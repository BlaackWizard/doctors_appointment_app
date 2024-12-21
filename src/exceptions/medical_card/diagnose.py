from fastapi import HTTPException, status

from src.exceptions.base import ApplicationException


class NotFoundDiagnoseException(ApplicationException):
    @property
    def message(self):
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Не удалось найти диагноз с таким ID, проверьте еще раз ID диагноза'
        )


class DiagnoseMedicalCardIsDifferentWithUsersMedicalCardException(ApplicationException):
    @property
    def message(self):
        return HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail='Мед.карта диагноза отличается от мед.карты пациента, проверьте еще раз ID пациента'
        )
