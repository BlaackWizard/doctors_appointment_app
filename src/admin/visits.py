from sqladmin import ModelView

from src.models.visits import Visits


class VisitsAdmin(ModelView, model=Visits):
    column_list = [
        Visits.visit_date,
        Visits.doctor,
        Visits.patient,
        Visits.medical_card,
    ]
    name = "Посещение"
    name_plural = "Посещения"
