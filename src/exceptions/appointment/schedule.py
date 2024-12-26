from fastapi import HTTPException, status

from src.exceptions.base import ApplicationException


class NotFoundScheduleException(ApplicationException):
    @property
    def message(self):
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Слот не найден, проверьте еще раз ID слота')


class SlotIsOccupiedException(ApplicationException):
    @property
    def message(self):
        return HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Этот слот уже занят')


class ThisScheduleAlreadyExistsException(ApplicationException):
    @property
    def message(self):
        return HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Этот слот уже есть в вашем расписаний!')


class DoctorCanNotChangeHisSlotWhilePatientsNotDoneTheirAppointmentException(ApplicationException):
    @property
    def message(self):
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Вы не можете изменить слот пока пользователи не посетят вас",
        )


class SlotNotBelongsToDoctorException(ApplicationException):
    @property
    def message(self):
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Слот ID не принадлежит врачу с ID врачом.",
        )
