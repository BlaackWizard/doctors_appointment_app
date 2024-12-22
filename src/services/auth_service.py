from dataclasses import dataclass
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, Request, Response, status
from jose import JWTError, jwt
from passlib.context import CryptContext

from src.config import settings
from src.exceptions.appointment.appointment import NotFoundAppointmentException
from src.exceptions.auth.auth_token import (TokenExpiredException,
                                            TokenIsNotValidException)
from src.exceptions.auth.user import (NotFoundUserException,
                                      NotFoundUserExceptionOrIncorrectPassword,
                                      UserAlreadyExistsException,
                                      UserNotFoundOrUserIsNotDoctorException)
from src.repos.base import BaseRepo
from src.repos.user import UserRepo
from src.tasks.send_email import send_reminder_email
from src.tasks.tasks_token import decode_url_safe_token

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
        raise UserNotFoundOrUserIsNotDoctorException().message

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
    appointment_repo: BaseRepo
    doctor_schedule_repo: BaseRepo

    async def authenticate(self, email: str, password: str):
        user = await self.repo.find_one(email=email)
        if not user or not verify_password(password, user.hashed_password):
            raise NotFoundUserExceptionOrIncorrectPassword().message

        return user

    async def register_user(self, user_data):
        existing_user = await self.repo.find_one(email=user_data.email)
        if existing_user:
            raise UserAlreadyExistsException().message
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

    async def verify_token(self, token: str):
        token_data = decode_url_safe_token(token)

        user_email = token_data.get('email')
        appointment_id = token_data.get('appointment_id')

        if user_email and appointment_id:
            user = await self.repo.find_one(email=user_email)
            appointment = await self.appointment_repo.find_one(id=appointment_id)
            if not user:
                raise NotFoundUserException().message

            if not appointment:
                raise NotFoundAppointmentException().message

            await self.appointment_repo.update(model_id=appointment.id, is_verified=True)

            schedule = await self.doctor_schedule_repo.find_one(id=appointment.schedule_id)

            await self.doctor_schedule_repo.update(model_id=schedule.id, status=False)

            appointment_time = appointment.date - timedelta(hours=24)

            send_reminder_email.apply_async(
                args=[user_email, appointment.date, "24 часа"],
                eta=appointment_time,
            )

            return Response('The appointment verified successfully!')

        return Response("Произошла ошибка")
