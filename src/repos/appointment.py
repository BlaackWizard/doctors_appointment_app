from ..models.appointment import AppointmentModel
from .sqlalchemy import SQLAlchemyRepo


class AppointmentRepo(SQLAlchemyRepo):
    model = AppointmentModel
