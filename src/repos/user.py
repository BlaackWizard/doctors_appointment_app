from .sqlalchemy import SQLAlchemyRepo
from ..models.user import UserModel


class UserRepo(SQLAlchemyRepo):
    model = UserModel
