from dataclasses import dataclass
from datetime import timedelta, datetime

from jose import jwt
from passlib.context import CryptContext

from src.config import settings
from src.exceptions.auth.not_found_user import NotFoundUserExceptionOrIncorrectPassword
from src.exceptions.auth.user_already_exists import UserAlreadyExistsException
from src.repos.base import BaseRepo

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
        to_encode, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM
    )
    return encoded_jwt


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
            role=user_data.role
        )
        return 'Пользователь успешно зарегистрирован'

    async def login_user(self, user_data):
        user = await self.authenticate(user_data.email, user_data.password)
        access_token = create_access_token({"sub": str(user.id)})
        return access_token
