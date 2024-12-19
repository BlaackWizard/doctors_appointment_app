from datetime import date
from typing import Optional

from pydantic import BaseModel


class SDiagnosis(BaseModel):
    medical_card_id: int
    diagnosis_text: str
    recommendation: str
    date: date


class SDiagnosisResponse(BaseModel):
    id: int # noqa
    diagnosis_text: str
    recommendation: Optional[str]
    medical_card_id: int

    class Config:
        orm_mode = True


class SVisits(BaseModel):
    medical_card_id: int
    visit_date: date
    doctor_name: str
    notes: Optional[str] = None


class STests(BaseModel):
    test_name: str
    result: str
    medical_card_id: str


class STestsResponse(STests):
    file: str
