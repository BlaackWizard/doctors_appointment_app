from typing import Annotated

from fastapi import APIRouter, Depends, Response

from src.schemas.auth import SUserLogin, SUserRegister
from src.services.auth_service import UserAuth

from .dependencies import user_services

router = APIRouter(prefix='/patient', tags=['Пациенты'])


@router.post('/register')
async def register_user_endpoint(
        user_data: SUserRegister,
        user_services: Annotated[UserAuth, Depends(user_services)],
):
    await user_services.register_user(
        user_data,
    )
    return Response("Пользователь успешно создан")


@router.post("/login")
async def login_user_endpoint(
    response: Response,
    user_data: SUserLogin,
    user_services: Annotated[UserAuth, Depends(user_services)],
):
    access_token = await user_services.login_user(user_data)
    response.set_cookie("user_access_token", access_token, httponly=True)

    return {"access_token": access_token}
