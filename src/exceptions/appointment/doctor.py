from fastapi import HTTPException, status

from src.exceptions.base import ApplicationException


class ThisIsNotYoursScheduleException(ApplicationException):
    @property
    def message(self):
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Это не ваш слот")


class NotFoundDoctorOrUserIsNotDoctorException(ApplicationException):
    @property
    def message(self):
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Не найден пользователь или пользовать не является врачом",
        )


class ThisIsAnotherDoctorException(ApplicationException):
    @property
    def message(self):
        return HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="ID врача отличается от ID врача в слоте, которой вы указали!",
        )
