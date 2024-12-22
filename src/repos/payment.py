from src.models.payment import Payment
from src.repos.sqlalchemy import SQLAlchemyRepo


class PaymentRepo(SQLAlchemyRepo):
    model = Payment
