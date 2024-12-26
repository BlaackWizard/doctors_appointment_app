from sqlalchemy import Column, Date, ForeignKey, Integer
from sqlalchemy.orm import relationship

from src.db.connect import Base


class Visits(Base):
    __tablename__ = "visits"

    id = Column(Integer, primary_key=True)  # noqa
    visit_date = Column(Date)
    doctor_id = Column(Integer, ForeignKey("users.id"))
    patient_id = Column(Integer, ForeignKey("users.id"))
    medical_card_id = Column(Integer, ForeignKey("medical_cards.id"), nullable=True)

    medical_card = relationship("MedicalCardModel", back_populates="visits")

    doctor = relationship("UserModel", back_populates="visit_doctor", foreign_keys=[doctor_id])
    patient = relationship("UserModel", back_populates="visit_patient", foreign_keys=[patient_id])

    def __str__(self):
        return f'Посещение: #{self.id}'
