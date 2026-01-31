from typing import Optional
from database import Base
from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import String,Integer,ForeignKey


class Doctor(Base):
    __tablename__ = "doctors"
    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(30))
    phone_number: Mapped[str] = mapped_column(String(13))
    

    patients: Mapped[list["Patient"]] = relationship(back_populates="doctor")


class Patient(Base):
    __tablename__ = "patients"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(30))
    age: Mapped[int] = mapped_column(Integer())
    phone_number: Mapped[str] = mapped_column(String(13))
    doctor_id: Mapped[int] = mapped_column(ForeignKey("doctors.id"))
    image: Mapped[Optional[str]] = mapped_column(nullable=True)
    video: Mapped[Optional[str]] = mapped_column(nullable=True)
    
    

    doctor: Mapped["Doctor"] = relationship(back_populates="patients")
     