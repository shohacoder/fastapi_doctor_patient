from typing import Optional
from pydantic import BaseModel




class DoctorCreate(BaseModel):
    full_name: str
    phone_number: str

class DoctorResponse(DoctorCreate):
    id: int

    class Config:
        from_attributes = True


class PatientCreate(BaseModel):
    full_name: str
    age: int
    phone_number: str
    doctor_id: int
    image: Optional[str] = None
    video: Optional[str] = None

class PatientResponse(PatientCreate):
    id: int
    
    class Config:
        from_attributes = True
