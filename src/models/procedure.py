from sqlalchemy import Column, String, Text, Date, Integer, ForeignKey
from sqlalchemy.orm import relationship

from src.db.connect import Base


class Procedure(Base):
    __tablename__ = "procedures"

    id = Column(Integer, primary_key=True, index=True) # noqa
    procedure_name = Column(String, nullable=False)
    description = Column(Text)
    date = Column(Date, nullable=False)
    doctor_id = Column(Integer, ForeignKey('users.id'))
    doctor_fullname = Column(String)
    medical_card_id = Column(Integer, ForeignKey('medical_cards.id'))

    medical_card = relationship("MedicalCardModel", back_populates="procedures")
