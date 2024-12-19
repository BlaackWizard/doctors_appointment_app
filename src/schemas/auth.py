import re
from typing import Literal

from pydantic import BaseModel, EmailStr, model_validator


class SUserRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    username: str
    phone_number: str
    role: Literal["patient", "doctor", "admin"] = "patient"

    @model_validator(mode="after")
    def validate_phone_number(cls, values):
        phone_pattern = re.compile(r"^\+?[1-9]\d{1,14}$")
        if not phone_pattern.match(values.phone_number):
            raise ValueError("Неверный формат номера телефона. Ожидается формат например, +123456789.")
        return values


class SUserLogin(BaseModel):
    email: EmailStr
    password: str
