from sqladmin import ModelView

from src.models.user import UserModel


class UserAdmin(ModelView, model=UserModel):
    column_list = [UserModel.id, UserModel.full_name, UserModel.role]
    column_details_exclude_list = [UserModel.hashed_password]

    name = "Пользователь"
    name_plural = "Пользователи"
