from fastapi import HTTPException, status

from src.exceptions.base import ApplicationException


class NotFoundProcedureException(ApplicationException):
    @property
    def message(self):
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Не удалось найти процедуру с этим ID",
        )


class ThisIsNotYourProcedureException(ApplicationException):
    @property
    def message(self):
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Врач не может редактировать чужую процедуру, проверьте еще раз ID процедуры",
        )


class ProcedureMedicalCardIsDifferentWithUserMedicalCardException(ApplicationException):
    @property
    def message(self):
        return HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="ID мед.карты процедуры отличается от ID карты пользователя."
                   "Проверьте еще раз ID пользователя",
        )
