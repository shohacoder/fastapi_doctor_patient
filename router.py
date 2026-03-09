from fastapi import APIRouter, Depends,Form, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from schemas import PatientCreate,PatientResponse
import crud


router = APIRouter(prefix="/patients",tags=["Patients"])

@router.post("/",response_model=PatientResponse)
async def create_patient_endpoint(
    full_name: str = Form(...),
    age: int = Form(...),
    phone_number: str = Form(...),
    doctor_id: int = Form(...),
    image: UploadFile = None,
    video: UploadFile = None,
    db: AsyncSession = Depends(get_db)
):
    patient = PatientCreate(full_name=full_name,age=age,phone_number=phone_number,doctor_id=doctor_id)
    return await crud.create_patient(patient,db,image,video)

@router.get("/",response_model=list[PatientResponse])
async def get_patients_endpoint(db: AsyncSession = Depends(get_db)):
    return await crud.read_patients(db)

@router.get("/{patient_id}",response_model=PatientResponse)
async def read_patient_endpoint(patient_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.read_patient(patient_id,db)

@router.put("/{patient_id}", response_model=PatientResponse)
async def update_patient_endpoint(patient_id: int, patient: PatientCreate, db: AsyncSession = Depends(get_db)):
    return await crud.update_patient(patient_id,patient,db)

@router.delete("/{patient_id}", response_model=dict)
async def delete_patient_endpoint(patient_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.delete_patient(patient_id,db)

