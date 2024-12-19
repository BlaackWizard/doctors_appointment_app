from fastapi import HTTPException, status

from src.exceptions.base import ApplicationException


class NotFoundScheduleException(ApplicationException):
    @property
    def message(self):
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Расписание не найдено')


class SlotIsOccupiedException(ApplicationException):
    @property
    def message(self):
        return HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Этот слот уже занят')
