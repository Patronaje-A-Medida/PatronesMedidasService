from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.controllers.body_measurements_controller import router as BodyMeasurementsRouter

app = FastAPI(title="API PATRONES Y MEDIDAS")

app.include_router(BodyMeasurementsRouter, tags=["Body Measurements"], prefix="/api/body-measurements")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Patrones y Medidas Api is running"}
