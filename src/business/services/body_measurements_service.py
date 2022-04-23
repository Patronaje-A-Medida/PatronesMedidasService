from unittest import result
import numpy as np
import cv2
import mediapipe as mp

from fastapi import Depends, UploadFile
from persistence.repositories.repositories import BodyMeasurementsRepository
from business.handlers.service_exception import ServiceException

mp_face_detection = mp.solutions.face_detection


class BodyMeasurementsService():
    def __init__(self, repository: BodyMeasurementsRepository = Depends(BodyMeasurementsRepository)) -> None:
        self.repository = repository

    async def get_all(self) -> list:
        result = await self.repository.get_all()
        return result

    async def take_measurements(self, file: UploadFile):
        content = await file.read()
        bytes_as_np_array = np.frombuffer(content, dtype=np.uint8)
        image = cv2.imdecode(bytes_as_np_array, cv2.IMREAD_COLOR)

        with  mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) as face_detection:
            results = face_detection.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            if not results.detections:
                raise ServiceException("No hay personas", 10005)
        
        # pre procesamiento 


        #prediccion con CNN

        # retornar el output de la CNN    
        return []

                
