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
        service: BodyMeasurementsService = Depends(BodyMeasurementsService)):
    try:
        res = await service.take_measurements(file_frontal, file_lateral, height, client_id)
        return {f'lista: {res}'}
    except ServiceException as ex:
        return JSONResponse(status_code=400, content={"error_message": ex.error_message},)
