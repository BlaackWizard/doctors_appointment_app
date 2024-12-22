from sqlalchemy import Column, Date, ForeignKey, Integer, String, Text, Float
from sqlalchemy.orm import relationship

from src.db.connect import Base


class Wallet(Base):
    __tablename__ = "wallet"

    id = Column(Integer, primary_key=True)
    balance = Column(Float, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))

