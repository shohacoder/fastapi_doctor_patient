import shutil
from fastapi import HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pathlib import Path

from models import *
from schemas import *
from database import MEDIA_DIR


async def create_doctor(doctor: DoctorCreate, db: AsyncSession) ->  DoctorResponse:
    db_doctor = Doctor(**doctor.model_dump())
    db.add(db_doctor)
    await db.commit()
    await db.refresh(db_doctor)
    return DoctorResponse.model_validate(db_doctor)


async def read_doctors(db: AsyncSession) -> list[DoctorResponse]:
    data = await db.execute(select(Doctor))
    return [DoctorResponse.model_validate(doctor) for doctor in data.scalars().all()]


async def read_doctor(doctor_id: int, db:AsyncSession) -> DoctorResponse:
    db_doctor = await db.get(Doctor, doctor_id)
    if db_doctor is None:
        raise HTTPException(status_code=404, detail="Doctor Not Found")
    return DoctorResponse.model_validate(db_doctor)


async def update_doctor(doctor_id: int, doctor: DoctorCreate, db: AsyncSession) -> DoctorResponse:
    db_doctor = await db.get(Doctor, doctor_id)
    if db_doctor is None:
        raise HTTPException(status_code=404, detail="Doctor Not Found")
    
    for key,value in doctor:
        setattr(db_doctor,key,value)

    await db.commit()
    await db.refresh(db_doctor)

    return DoctorResponse.model_validate(db_doctor)


async def delete_doctor(doctor_id: int, db: AsyncSession) -> dict:
    db_doctor = await db.get(Doctor, doctor_id)
    if db_doctor is None:
        raise HTTPException(status_code=404, detail="Doctor Not Found")
    
    await db.delete(db_doctor)
    await db.commit()
    return {"message": "Doctor deleted successfully"}



async def create_patient(patient: PatientCreate, db: AsyncSession,image:UploadFile=None, video: UploadFile=None) -> PatientResponse:
    if image: 
        image_extension = image.filename.lower().split(".")[-1]
        if image_extension not in ["jpg","jpeg","png"]:
            raise HTTPException(status_code=400, detail="fqat jpg va png formatlariga ruxsat bor")
        
    if video:
        video_extension = video.filename.lower().split(".")[-1]
        if video_extension not in ["mp4"]:
            raise HTTPException(status_code=400, detail="faqat mp4 formatidagi videoga ruxsat")
    db_patient = Patient(**patient.model_dump())
    db.add(db_patient)
    await db.commit()
    await db.refresh(db_patient) 
    

    if image:
        image_path = Path(MEDIA_DIR) / f"patient_{db_patient.id}_image.{image_extension}"
        with image_path.open("wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        db_patient.image = str(image_path)

    if video:
        video_path = Path(MEDIA_DIR) / f"patient_{db_patient.id}_video.{video_extension}"
        with video_path.open("wb") as buffer:
            shutil.copyfileobj(video.file, buffer)
        db_patient.video = str(video_path)

    await db.commit()
    await db.refresh(db_patient)
    return PatientResponse.model_validate(db_patient)

        




async def read_patients(db: AsyncSession) -> list[PatientResponse]:
    data = await db.execute(select(Patient))
    return [PatientResponse.model_validate(patient) for patient in data.scalars().all()]

async def read_patient(patient_id: int, db: AsyncSession) -> PatientResponse:
    db_patient = await db.get(Patient,patient_id)

    if db_patient is None:
        raise HTTPException(404,"Patient Not Found")
    return PatientResponse.model_validate(db_patient)

async def update_patient(patient_id: int, patient: PatientCreate, db: AsyncSession) -> PatientResponse:
    db_patient = await db.get(Patient, patient_id)
    if db_patient is None:
        raise HTTPException(status_code=404,detail="Patient Not Found")
    for key,value in patient:
        setattr(db_patient,key,value)

    await db.commit()
    await db.refresh(db_patient)
    return PatientResponse.model_validate(db_patient)

async def delete_patient(patient_id: int,db: AsyncSession) -> dict:
    db_patient = await db.get(Patient, patient_id)

    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient Not Found")
    
    await db.delete(db_patient)
    await db.commit()
    return {"message": "Patient deleted successfully"}

