from sqladmin import ModelView
from src.models.doctor_schedule import DoctorScheduleModel


class DoctorScheduleAdmin(ModelView, model=DoctorScheduleModel):
    column_list = [
        DoctorScheduleModel.id,
        DoctorScheduleModel.doctor,
        DoctorScheduleModel.start_time,
        DoctorScheduleModel.end_time,
        DoctorScheduleModel.is_available
    ]

    name = "Слот врача"
    name_plural = "Слоты врача"
