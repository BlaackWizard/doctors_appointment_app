from src.repos.user import UserRepo
from src.services.auth_service import UserAuth


def user_services():
    return UserAuth(UserRepo)
