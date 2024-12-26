from sqladmin import ModelView
from src.models.appointment import AppointmentModel


class AppointmentAdmin(ModelView, model=AppointmentModel):
    column_list = [
        AppointmentModel.id,
        AppointmentModel.doctor,
        AppointmentModel.patient,
        AppointmentModel.status,
        AppointmentModel.is_verified,
    ]
    name = "Запись"
    name_plural = "Записи"
