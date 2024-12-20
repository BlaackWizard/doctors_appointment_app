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


class PatientDoctorConflictException(ApplicationException):
    @property
    def message(self):
        return HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пациент не завершал прием у врача с данным ID. Посетите врача и после вы можете создать мед.карту',
        )


class BeforeCreateVisitPatientMustCreateAppointmentException(ApplicationException):
    @property
    def message(self):
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Для того чтобы создать посещение, '
                   'Пациент должен отправить вам запись на посещение',
        )


class ThisUserIsNotDoctorException(ApplicationException):
    @property
    def message(self):
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Этот пользователь не является врачом, проверьте еще раз ID врача',
        )
