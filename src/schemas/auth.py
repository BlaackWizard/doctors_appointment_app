import re
from typing import Literal

from pydantic import BaseModel, EmailStr, Field, model_validator


class SUserRegister(BaseModel):
    email: EmailStr = Field(alias="Эл.почта")
    password: str = Field(alias="Пароль")
    full_name: str = Field(alias="ФИО")
    username: str = Field(alias="Логин")
    phone_number: str = Field(alias="Номер телефона")
    role: Literal["patient", "doctor", "admin"] = "patient"

    @model_validator(mode="after")
    def validate_phone_number(cls, values):
        phone_pattern = re.compile(r"^\+?[1-9]\d{1,14}$")
        if not phone_pattern.match(values.phone_number):
            raise ValueError("Неверный формат номера телефона. Ожидается формат например, +123456789.")
        return values


class SUserLogin(BaseModel):
    username: str = Field(alias="Логин")
    password: str = Field(alias="Пароль")
