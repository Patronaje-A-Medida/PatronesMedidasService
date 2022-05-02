from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from business.services.body_measurements_service import BodyMeasurementsService
from business.handlers.service_exception import ServiceException

router = APIRouter()


@router.get("")
async def get_all(service: BodyMeasurementsService = Depends(BodyMeasurementsService)):
    docs = await service.get_all()
    return {"docs": docs}


@router.post("/compute-measurements/{client_id}")
async def take_measurements(
        client_id: int,
        file_frontal: UploadFile = File(...),
        file_lateral: UploadFile = File(...),
        height: float = Form(...),
        service: BodyMeasurementsService = Depends(BodyMeasurementsService)) -> dict:
    try:
        result = await service.take_measurements(file_frontal, file_lateral, height, client_id)
        return result.to_map()
    except ServiceException as ex:
        return JSONResponse(status_code=400, content={"error_message": ex.error_message},)

@router.get("/last-measurements/{client_id}")
async def last_measurements(client_id: int, service: BodyMeasurementsService = Depends(BodyMeasurementsService)) -> dict:
    try:
        result = await service.get_last_measurements(client_id)
        return result.to_map()
        
    except ServiceException as ex:
        return JSONResponse(status_code=400, content={"error_message": ex.error_message},)