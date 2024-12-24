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
        phone_number = values.phone_number

        if len(phone_number) != 13:
            raise ValueError("Номер телефона должен содержать 13 символов, включая код страны (+998).")

        if not phone_number.startswith('+998'):
            raise ValueError("Номер телефона должен начинаться с кода страны +998.")

        if not phone_number[4:].isdigit():
            raise ValueError("Номер телефона должен содержать только цифры после кода страны.")

        return values


class SUserLogin(BaseModel):
    username: str = Field(alias="Логин")
    password: str = Field(alias="Пароль")
