from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from business.services.body_measurements_service import BodyMeasurementsService
from business.handlers.service_exception import ServiceException
from domain.utils.constants import FIREBASE_CONFIG, ADM_CREDENTIALS
import pyrebase
import os



firebase = pyrebase.initialize_app(FIREBASE_CONFIG)
storage = firebase.storage()
auth = firebase.auth()
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
        user = auth.sign_in_with_email_and_password(ADM_CREDENTIALS[0], ADM_CREDENTIALS[1])
        result = await service.take_measurements(file_frontal, file_lateral, height, client_id)
        await upload_temp_files(file_frontal.filename, user['idToken'])
        await upload_temp_files(file_lateral, user['idToken'])
        #await storage.child('data/'+file_lateral.filename).put(file_lateral.file, user['idToken'])
        os.remove('./src/business/tmp/'+file_frontal.filename)
        return JSONResponse(status_code=200, content=result.to_map())
    except ServiceException as ex:
        return JSONResponse(status_code=500, content={"statusCode": 500, "errorCode": ex.error_code, "message": ex.error_message})

@router.get("/last-measurements/{client_id}")
async def last_measurements(client_id: int, service: BodyMeasurementsService = Depends(BodyMeasurementsService)) -> dict:
    try:
        result = await service.get_last_measurements(client_id)
        if result is None:
            return JSONResponse(status_code=404, content={"statusCode": 404, "errorCode": 10010, "message": "El usuario no cuenta con medidas corporales tomadas"})
        return JSONResponse(status_code=200, content=result.to_map())
    except ServiceException as ex:
        return JSONResponse(status_code=400, content={"statusCode": 500, "errorCode": ex.error_code, "message": ex.error_message})

async def upload_temp_files(file: any, token: any): 
    if isinstance(file, str):
        storage.child('data/'+file).put('./src/business/tmp/'+file, token)
    else:
        storage.child('data/'+file.filename).put(file.file, token)
    
