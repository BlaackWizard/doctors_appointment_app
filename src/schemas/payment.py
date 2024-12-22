from typing import Literal

from pydantic import BaseModel, Field


class SPaymentRequest(BaseModel):
    service_id: int = Field(alias='ID услуги')
    payment_method: Literal["Наличными", "Через карту"]


class SPaymentResponse(BaseModel):
    message: str
    balance: float
