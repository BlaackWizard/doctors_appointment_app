from fastapi import HTTPException, status

from src.exceptions.base import ApplicationException


class NotFoundUserException(ApplicationException):
    @property
    def message(self):
        return HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Данный пользователь не найден в базе данных')


class NotFoundUserExceptionOrIncorrectPassword(ApplicationException):
    @property
    def message(self):
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Неправильный логин или пароль',
        )


class NotFoundUserByIDException(ApplicationException):
    @property
    def message(self):
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Не найден врач по этому ID')


class UserAlreadyExistsException(ApplicationException):
    @property
    def message(self):
        return HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователь с данным логином уже существует',
        )


class UserNotFoundOrUserIsNotDoctorException(ApplicationException):
    @property
    def message(self):
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Врач не найден в базе данных или пользователь не является врачом. "
                   "Пожалуйста войди в систему как врач",
        )


class UserNotPatientException(ApplicationException):
    @property
    def message(self):
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Данный пользователь не является пациентом, пожалуйста зарегистрируйтесь и потом войдите в систему',
        )


class PermissionDeniedForUserException(ApplicationException):
    @property
    def message(self):
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Доступ к ресурсу запрещен',
        )
