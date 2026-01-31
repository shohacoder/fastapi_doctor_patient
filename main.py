from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from database import Base,engine,get_db,MEDIA_DIR
from sqlalchemy.ext.asyncio import AsyncSession
import uvicorn
from schemas import *
import crud
from router import router as patient_router

app = FastAPI()
app.mount(f"/{MEDIA_DIR}",StaticFiles(directory="media"), name="media")

async def init_db():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

@app.on_event("startup")
async def startup_event():
    await init_db()

@app.post("/doctors/",response_model=DoctorResponse)  
async def create_doctor_endpoint(doctor: DoctorCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_doctor(doctor,db)

@app.get("/doctors/",response_model=list[DoctorResponse])
async def read_doctors_endpoint(db: AsyncSession = Depends(get_db)):
    return await crud.read_doctors(db)

@app.get("/doctors/{doctor_id}",response_model=DoctorResponse)
async def read_doctor_endpoint(doctor_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.read_doctor(doctor_id,db)

@app.put("/doctors/{doctor_id}",response_model=DoctorResponse)
async def update_doctor_endpoint(doctor_id: int, doctor: DoctorCreate, db: AsyncSession = Depends(get_db)):
    return await crud.update_doctor(doctor_id,doctor,db)

@app.delete("/doctors/{doctor_id}",response_model=dict)
async def delete_doctor_endpoint(doctor_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.delete_doctor(doctor_id,db)

app.include_router(patient_router)


if __name__ == "__main__":
    uvicorn.run(app)