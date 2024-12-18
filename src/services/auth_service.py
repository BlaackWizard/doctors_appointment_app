from dataclasses import dataclass
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, Request, status
from jose import JWTError, jwt
from passlib.context import CryptContext

from src.config import settings
from src.exceptions.auth.token import (TokenExpiredException,
                                       TokenIsNotValidException)
from src.exceptions.auth.user import (NotFoundUserExceptionOrIncorrectPassword,
                                      UserAlreadyExistsException,
                                      UserNotFoundOrUserIsNotDoctorException)
from src.repos.base import BaseRepo
from src.repos.user import UserRepo

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now() + timedelta(days=30)
    to_encode.update({"exp": int(expire.timestamp())})
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM,
    )
    return encoded_jwt


def get_token(request: Request):
    token = request.cookies.get("user_access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="не найден токен")
    return token


async def get_current_doctor(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM)
    except JWTError as e:
        print(f"JWTError: {e}")
        raise TokenIsNotValidException()

    expire: int = payload.get("exp")
    if not expire or int(expire) < int(datetime.now().timestamp()):
        raise TokenExpiredException()

    user_id: str = payload.get("sub")
    if not user_id:
        raise

    user = await UserRepo.find_one(id=int(user_id))
    if not user or str(user.role) != "doctor":
        raise UserNotFoundOrUserIsNotDoctorException()

    return user


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM)
    except JWTError as e:
        print(f"JWTError: {e}")
        raise TokenIsNotValidException()

    expire: int = payload.get("exp")
    if not expire or int(expire) < int(datetime.now().timestamp()):
        raise TokenExpiredException()

    user_id: str = payload.get("sub")
    if not user_id:
        raise

    user = await UserRepo.find_one(id=int(user_id))
    if not user:
        raise UserNotFoundOrUserIsNotDoctorException()

    return user


@dataclass
class UserAuth:
    repo: BaseRepo

    async def authenticate(self, email: str, password: str):
        user = await self.repo.find_one(email=email)
        if not user or not verify_password(password, user.hashed_password):
            raise NotFoundUserExceptionOrIncorrectPassword()

        return user

    async def register_user(self, user_data):
        existing_user = await self.repo.find_one(email=user_data.email)
        if existing_user:
            raise UserAlreadyExistsException()
        hashed_password = get_password_hash(user_data.password)
        await self.repo.add(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_password,
            full_name=user_data.full_name,
            phone_number=user_data.phone_number,
            role=user_data.role,
        )
        return "Пользователь успешно создан, теперь войдите в систему"

    async def login_user(self, user_data):
        user = await self.authenticate(user_data.email, user_data.password)
        access_token = create_access_token({"sub": str(user.id)})
        return access_token
