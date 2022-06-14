from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from business.services.body_measurements_service import BodyMeasurementsService
from business.handlers.service_exception import ServiceException
import pyrebase

config = {
    "apiKey": "AIzaSyD6rwCtpBQrIVLah_BFVjGjt6W4XUwYfPw",
    "authDomain": "pry2021251-pam.firebaseapp.com",
    "databaseURL": "",
    "projectId": "pry2021251-pam",
    "storageBucket": "pry2021251-pam.appspot.com",
    "messagingSenderId": "101974237012",
    "appId": "1:101974237012:web:38e2c349736ecf2fbe32c1"
}

firebase = pyrebase.initialize_app(config)
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
        #result = await service.take_measurements(file_frontal, file_lateral, height, client_id)
        #return JSONResponse(status_code=200, content=result.to_map())
        user = auth.sign_in_with_email_and_password('u201716506@upc.edu.pe', 'cocobicho1413')
        storage.child('data/'+file_frontal.filename).put(file_frontal.file, user['idToken'])
        storage.child('data/'+file_lateral.filename).put(file_lateral.file, user['idToken'])
        return JSONResponse(status_code=200, content={'ok':'ok'})
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
