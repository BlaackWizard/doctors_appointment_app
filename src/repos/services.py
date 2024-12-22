from src.models.services import Services
from src.repos.sqlalchemy import SQLAlchemyRepo


class ServiceRepo(SQLAlchemyRepo):
    model = Services
