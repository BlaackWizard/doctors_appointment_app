from sqlalchemy import Column, String, Integer, Enum
from sqlalchemy.orm import relationship

from src.db.connect import Base


class UserRoleEnum(str, Enum):
    PATIENT = "patient"
    DOCTOR = "doctor"
    ADMIN = "admin"


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    full_name = Column(String, nullable=False)
    username = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum('patient', 'doctor', 'admin', name='role_type'), default=UserRoleEnum.PATIENT)

    schedules = relationship("DoctorScheduleModel", back_populates="doctor", cascade="all, delete-orphan")

