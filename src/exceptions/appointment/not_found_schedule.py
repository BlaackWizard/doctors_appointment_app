from src.exceptions.base import ApplicationException


class NotFoundScheduleException(ApplicationException):
    @property
    def message(self):
        return 'Расписание не найдено'


class SlotIsOccupiedException(ApplicationException):
    @property
    def message(self):
        return 'Этот слот уже занят'

