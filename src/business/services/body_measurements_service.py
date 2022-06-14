from datetime import datetime
from re import U
from typing import List
import numpy as np
import cv2
import mediapipe as mp

from fastapi import Depends, UploadFile
from persistence.repositories.repositories import BodyMeasurementsRepository
from business.handlers.service_exception import ServiceException
from business.machine_learning.measurement_predictive_model import MeasurementPredictiveModel
from domain.entities.body_measurements import BodyMeasurements
from domain.entities.measurement import Measurement
from business.mapper.mapper import Mapper
from domain.models.measurements.body_measurements_read import BodyMeasurementsRead

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


class BodyMeasurementsService():
    def __init__(
            self,
            repository: BodyMeasurementsRepository = Depends(BodyMeasurementsRepository),
            predictive_model: MeasurementPredictiveModel = Depends(MeasurementPredictiveModel),
            mapper: Mapper = Depends(Mapper)) -> None:
        self.repository = repository
        self.predictive_model = predictive_model
        self.mapper = mapper

    async def get_all(self) -> list:
        result = await self.repository.get_all()
        return result

    async def get_last_measurements(self, client_id: int) -> BodyMeasurementsRead:
        result = await self.repository.get_last_measurements(client_id)
        if result is None:
            return None
        result_read = self.mapper.map_to_body_measurements_read(result)
        return result_read

    async def take_measurements(
            self,
            image_frontal_file: UploadFile,
            image_lateral_file: UploadFile,
            height: float,
            client_id: int) -> BodyMeasurementsRead:
        content_frontal = await image_frontal_file.read()
        bytes_as_np_array_1 = np.frombuffer(content_frontal, dtype=np.uint8)
        image_frontal = cv2.imdecode(bytes_as_np_array_1, cv2.IMREAD_COLOR)

        cv2.imwrite('./src/business/tmp/'+image_frontal_file.filename, image_frontal)

        """content_lateral = await image_lateral_file.read()
        bytes_as_np_array_2 = np.frombuffer(content_lateral, dtype=np.uint8)
        image_lateral = cv2.imdecode(bytes_as_np_array_2, cv2.IMREAD_COLOR)"""

        with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) as face_detection:
            results = face_detection.process(
                cv2.cvtColor(image_frontal, cv2.COLOR_BGR2RGB))
            if not results.detections:
                raise ServiceException(
                    "Las imágenes tomadas no pertenecen a una persona", 10020)

        """with  mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) as face_detection:
            results = face_detection.process(cv2.cvtColor(image_2, cv2.COLOR_BGR2RGB))
            if not results.detections:
                raise ServiceException("No hay personas", 10005)"""

        dict_measurements = self.predictive_model.predict(image_frontal)

        entity = BodyMeasurements(
            client_id=client_id,
            measurement_date=datetime.now(),
            measurements=[
                Measurement(name_measurement='altura', value=height, acronym='H', units='cm'),
                Measurement(name_measurement='contorno de pecho', value=dict_measurements['Bust_Circ'], acronym='Bc', units='cm'),
                Measurement(name_measurement='contorno de cintura', value=dict_measurements['TrouserWAIST_Circ'], acronym='Wc', units='cm'),
                Measurement(name_measurement='contorno de cintura natural', value=dict_measurements['NaturalWAIST_Circ'], acronym='NWc', units='cm'),
                Measurement(name_measurement='contorno de cadera alta', value=dict_measurements['HIP_Circ'], acronym='Hc', units='cm'),
                Measurement(name_measurement='contorno de cadera baja', value=dict_measurements['Hip_2_Circ'], acronym='Hc2', units='cm'),
                Measurement(name_measurement='alto de talle de espalda', value=dict_measurements['NECK_Height'] - dict_measurements['TrouserWaist_Height_Back'], acronym='SWb', units='cm'),
                Measurement(name_measurement='alto de talle delantero', value=dict_measurements['NECK_Height'] - dict_measurements['TrouserWaist_Height_Front'], acronym='SWf', units='cm'),
                Measurement(name_measurement='alto de pecho', value=dict_measurements['SideNeck_to_Bust'], acronym='Bh', units='cm'),
                Measurement(name_measurement='alto de cadera alta', value=dict_measurements['Hip_Height'], acronym='Hh', units='cm'),
                Measurement(name_measurement='alto de cadera baja', value=dict_measurements['Hip_2_Height'], acronym='Hh2', units='cm'),
                Measurement(name_measurement='separación del pecho', value=dict_measurements['Bust_to_Bust'], acronym='BB', units='cm'),
                Measurement(name_measurement='ancho de espalda', value=dict_measurements['Across_Back'], acronym='bw', units='cm'),
                Measurement(name_measurement='ancho de busto', value=dict_measurements['Across_Front'], acronym='fw', units='cm'),
                Measurement(name_measurement='contorno del cuello', value=dict_measurements['NeckBase_Circ'], acronym='Nc', units='cm'),
                Measurement(name_measurement='ancho de hombro', value=dict_measurements['Shoulder_Length'], acronym='Sh', units='cm'),
                Measurement(name_measurement='largo de brazo', value=dict_measurements['Shoulder_to_Wrist'], acronym='Al', units='cm'),
                Measurement(name_measurement='contorno de brazo', value=dict_measurements['Bicep_Circ'], acronym='Ac', units='cm'),
                Measurement(name_measurement='contorno de muñeca', value=dict_measurements['Wrist_Circ'], acronym='Wrc', units='cm'),
                Measurement(name_measurement='tiro al suelo', value=dict_measurements['Inseam'], acronym='Is', units='cm'),
                Measurement(name_measurement='entrepierna delantera', value=dict_measurements['CrotchLength_Front'], acronym='Crf', units='cm'),
                Measurement(name_measurement='entrepierna trasera', value=dict_measurements['CrotchLength_Back'], acronym='Crb', units='cm'),
                Measurement(name_measurement='contorno de muslo', value=dict_measurements['Thigh_Circ'], acronym='Tc', units='cm'),
                Measurement(name_measurement='contorno de pantorrilla', value=dict_measurements['Calf_Circ'], acronym='Cfc', units='cm'),
                Measurement(name_measurement='contorno de rodilla', value=dict_measurements['Knee_Circ'], acronym='Kc', units='cm'),
            ]
        )

        inserted_id = await self.repository.insert(entity)
        entity.id = inserted_id

        model = self.mapper.map_to_body_measurements_read(entity)
        await image_frontal_file.close()
        return model
  