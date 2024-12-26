from sqladmin import ModelView

from src.models.medical_card import MedicalCardModel


class MedicalCardAdmin(ModelView, model=MedicalCardModel):
    column_list = [
        MedicalCardModel.patient,
        MedicalCardModel.doctor,
        MedicalCardModel.patient_fullname,
        MedicalCardModel.birth_day,
        MedicalCardModel.contacts,
    ]
    name = 'Мед.карта'
    name_plural = "Мед.карты"
