from sqladmin import ModelView
from src.models.payment import Payment


class PaymentAdmin(ModelView, model=Payment):
    column_list = [
        Payment.patient,
        Payment.service,
        Payment.amount,
        Payment.date,
        Payment.is_paid,
    ]
    name = "Платёж"
    name_plural = "Платежи"
