from sqlalchemy import Column, Date, ForeignKey, Integer, String, Text, Float
from sqlalchemy.orm import relationship

from src.db.connect import Base


class Services(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True)

    title = Column(String, nullable=False)
    cost = Column(Float, nullable=False)
    requisites = Column(String, nullable=False)
