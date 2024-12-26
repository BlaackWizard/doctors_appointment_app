from fastapi import HTTPException, status

from src.exceptions.base import ApplicationException


class BeforeCreateVisitPatientMustCreateAppointmentException(ApplicationException):
    @property
    def message(self):
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Для того чтобы создать посещение, '
                   'Пациент должен записаться к врачу',
        )
