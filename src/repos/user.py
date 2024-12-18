from ..models.user import UserModel
from .sqlalchemy import SQLAlchemyRepo


class UserRepo(SQLAlchemyRepo):
    model = UserModel
