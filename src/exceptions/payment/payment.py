from fastapi import HTTPException, status

from src.exceptions.base import ApplicationException


class NotHaveEnoughMoneyException(ApplicationException):
    @property
    def message(self):
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='У вас недостаточно средств на вашем кошельке для того чтобы оплатить услугу',
        )


class NotFoundPaymentException(ApplicationException):
    @property
    def message(self):
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Платеж не найден',
        )


class ThisIsNotYourReceiptException(ApplicationException):
    @property
    def message(self):
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Это не ваш чек!',
        )
