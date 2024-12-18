from typing import Optional, Literal
from pydantic import BaseModel, EmailStr, Field

from src.models.user import UserRoleEnum


class SUserRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    username: str
    phone_number: str
    role: Literal["patient", "doctor", "admin"] = "patient"


class SUserLogin(BaseModel):
    email: EmailStr
    password: str
