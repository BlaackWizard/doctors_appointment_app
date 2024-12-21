from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class SDiagnosis(BaseModel):
    diagnosis_text: str = Field(alias="Текст диагноза")
    recommendation: str = Field(alias="Рекомендаций")
    patient_id: int = Field(alias='ID пациента')


class SDiagnosisResponse(BaseModel):
    diagnosis_id: int  # noqa
    diagnosis_text: str
    recommendation: Optional[str] = None
    medical_card_id: int

    class Config:
        orm_mode = True


class SVisits(BaseModel):
    patient_id: int
    visit_date: date = Field(alias="Дата визита")


class SProcedure(BaseModel):
    procedure_name: str = Field(alias="Название процедуры")
    description: str = Field(alias="Описание процедуры")
    notes: Optional[str] = Field(alias='Дополнительные комментарии', default=None)


class SCreateMedicalCard(BaseModel):
    doctor_id: int = Field("ID врача")
    birth_day: date = Field("Дата рождения")
    contacts: str = Field("Контакты")
