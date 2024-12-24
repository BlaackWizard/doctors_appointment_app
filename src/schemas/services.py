from pydantic import BaseModel, Field


class SServiceRequest(BaseModel):
    title: str = Field(alias='Название услуги')
    cost: float = Field(alias='Цена услуги')
    requisites: str = Field(alias='Реквизиты')


class SServiceResponse(BaseModel):
    message: str
    title: str
    cost: float
    requisites: str
    service_id: int
