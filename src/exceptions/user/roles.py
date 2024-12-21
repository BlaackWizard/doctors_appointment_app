from fastapi import HTTPException, status

from src.exceptions.base import ApplicationException


class ThisUserIsNotDoctorException(ApplicationException):
    @property
    def message(self):
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Этот пользователь не является врачом, проверьте еще раз ID врача',
        )


class PatientDoctorConflictException(ApplicationException):
    @property
    def message(self):
        return HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пациент не посетил данного врача, пройдите обследование и можете создать свою мед.карту',
        )


class YouAreNotDoctorException(ApplicationException):
    @property
    def message(self):
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Вы не являетесь врачом!")


class YouAreNotPatientException(ApplicationException):
    @property
    def message(self):
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Вы не являетесь пациентом, пройдите регистрацию",
        )
