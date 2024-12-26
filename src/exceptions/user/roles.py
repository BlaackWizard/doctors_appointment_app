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
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Пользователь не найден в базе данных или пользователь не является врачом",
        )


class YouAreNotPatientException(ApplicationException):
    @property
    def message(self):
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Вы не являетесь пациентом, пройдите регистрацию",
        )


class YouAreNotAdminException(ApplicationException):
    @property
    def message(self):
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Этот метод можно вызвать только администраторам',
        )
