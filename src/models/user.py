from datetime import date

from sqlalchemy import Column, Date, Enum, Integer, String
from sqlalchemy.orm import relationship

from src.db.connect import Base


class UserRoleEnum(str, Enum):
    PATIENT = "patient"
    DOCTOR = "doctor"
    ADMIN = "admin"


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)  # noqa
    full_name = Column(String, nullable=False)
    username = Column(String, nullable=False, unique=True)
    phone_number = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum('patient', 'doctor', 'admin', name='role_type'), default=UserRoleEnum.PATIENT)

    date = Column(Date, default=date.today())
    schedules = relationship("DoctorScheduleModel", back_populates="doctor", cascade="all, delete-orphan")

    appointment_with_doctor = relationship(
        "AppointmentModel",
        back_populates="doctor",
        foreign_keys="[AppointmentModel.doctor_id]",
    )
    appointment_with_patient = relationship(
        "AppointmentModel",
        back_populates="patient",
        foreign_keys="[AppointmentModel.patient_id]",
    )
    medical_cards_as_patient = relationship(
        "MedicalCardModel",
        back_populates="patient",
        foreign_keys="[MedicalCardModel.patient_id]",
    )
    medical_cards_as_doctor = relationship(
        "MedicalCardModel",
        back_populates="doctor",
        foreign_keys="[MedicalCardModel.doctor_id]",
    )
    payment_patient = relationship(
        "Payment",
        back_populates="patient",
        foreign_keys="[Payment.patient_id]",
    )
    schedules = relationship(
        "DoctorScheduleModel",
        back_populates="doctor",
        foreign_keys='[DoctorScheduleModel.doctor_id]',
    )
    visit_doctor = relationship(
        "Visits",
        back_populates="doctor",
        foreign_keys='[Visits.doctor_id]',
    )
    visit_patient = relationship(
        "Visits",
        back_populates="patient",
        foreign_keys='[Visits.patient_id]',
    )

    def __str__(self):
        return f"Пользователь {self.full_name}"
