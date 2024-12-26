from fastapi import HTTPException
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse
from src.services.auth_service import create_access_token, get_user_by_token
from src.api.patients.dependencies import user_services
from src.exceptions.auth.user import NotFoundUserExceptionOrIncorrectPassword


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        try:
            user_service = user_services()
            user = await user_service.authenticate(username, password)
        except NotFoundUserExceptionOrIncorrectPassword:
            raise HTTPException(status_code=401, detail="Неверные имя пользователя или пароль")

        if user and user.role == "admin":
            access_token = create_access_token({"sub": str(user.id)})
            request.session.update({"token": access_token})
            return True
        else:
            raise HTTPException(status_code=403, detail="Доступ разрешен только для администраторов")

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:

        token = request.session.get("token")

        if not token:
            return False

        try:
            user = await get_user_by_token(token, role="admin")
            if user and user.role == "admin":
                return True
        except Exception:
            pass

        return False


authentication_backend = AdminAuth(secret_key='....')
