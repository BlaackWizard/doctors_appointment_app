from .sqlalchemy import SQLAlchemyRepo
from ..models.appointment import AppointmentModel


class AppointmentRepo(SQLAlchemyRepo):
    model = AppointmentModel
