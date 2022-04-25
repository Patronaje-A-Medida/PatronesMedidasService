from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from business.services.body_measurements_service import BodyMeasurementsService
from business.handlers.service_exception import ServiceException

router = APIRouter()


@router.get("")
async def get_all(service: BodyMeasurementsService = Depends(BodyMeasurementsService)):
    docs = await service.get_all()
    return {"docs": docs}


@router.post("/compute-measurements")
async def take_measurements(file: UploadFile = File(...) ,file2: UploadFile = File(...) ,height: float= Form(...) ,
 service: BodyMeasurementsService = Depends(BodyMeasurementsService)):
    try:
        res = await service.take_measurements(file,file2,height)
        return {"lista": res}
    except ServiceException as ex: 
        return JSONResponse(status_code=400, content={"error_message": ex.error_message},)

