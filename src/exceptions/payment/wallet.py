from fastapi import HTTPException, status

from src.exceptions.base import ApplicationException


class NotFoundWalletException(ApplicationException):
    @property
    def message(self):
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Не удалось найти ваш кошелек'
        )


class WalletAlreadyExistsException(ApplicationException):
    @property
    def message(self):
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='У вас уже есть кошелек'
        )
