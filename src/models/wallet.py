from sqlalchemy import Column, Float, ForeignKey, Integer

from src.db.connect import Base


class Wallet(Base):
    __tablename__ = "wallet"

    id = Column(Integer, primary_key=True) # noqa

    balance = Column(Float, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    def __str__(self):
        return f'Кошелек: #{self.id}'
