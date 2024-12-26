from sqladmin import ModelView
from src.models.services import Services


class ServicesAdmin(ModelView, model=Services):
    column_list = [
        Services.title,
        Services.cost,
        Services.requisites,
    ]
    name = "Услуга"
    name_plural = "Услуги"
