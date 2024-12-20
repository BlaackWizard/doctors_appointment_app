from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.db.connect import Base


class MedicalCardModel(Base):
    __tablename__ = "medical_cards"

    id = Column(Integer, primary_key=True)  # noqa
    patient_id = Column(Integer, ForeignKey('users.id'))
    doctor_id = Column(Integer, ForeignKey('users.id'))
    doctor_fullname = Column(String, nullable=False)
    patient_fullname = Column(String, nullable=False)
    birth_day = Column(Date, nullable=False)
    contacts = Column(String, nullable=False)

    visits = relationship("Visits", back_populates="medical_card")
    diagnosis = relationship("Diagnosis", back_populates="medical_card")
    analyzes = relationship("Analyzes", back_populates="medical_card")
    procedures = relationship("Procedure", back_populates="medical_card")
