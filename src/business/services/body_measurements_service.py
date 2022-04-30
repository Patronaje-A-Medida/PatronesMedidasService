from datetime import datetime
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

    async def take_measurements(
            self,
            image_frontal_file: UploadFile,
            image_lateral_file: UploadFile,
            height: float,
            client_id: int) -> BodyMeasurementsRead:
        content_frontal = await image_frontal_file.read()
        bytes_as_np_array_1 = np.frombuffer(content_frontal, dtype=np.uint8)
        image_frontal = cv2.imdecode(bytes_as_np_array_1, cv2.IMREAD_COLOR)

        content_lateral = await image_lateral_file.read()
        bytes_as_np_array_2 = np.frombuffer(content_lateral, dtype=np.uint8)
        image_lateral = cv2.imdecode(bytes_as_np_array_2, cv2.IMREAD_COLOR)

        """with  mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) as face_detection:
            results = face_detection.process(cv2.cvtColor(image_1, cv2.COLOR_BGR2RGB))
            if not results.detections:
                raise ServiceException("No hay personas", 10005)

        

        with  mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) as face_detection:
            results = face_detection.process(cv2.cvtColor(image_2, cv2.COLOR_BGR2RGB))
            if not results.detections:
                raise ServiceException("No hay personas", 10005)"""

        arr_measurements = self.predictive_model.predict(
            image_frontal, image_lateral, height)

        entity = BodyMeasurements(
            client_id=client_id,
            measurement_date=datetime.now(),
            measurements=[
                Measurement(name_measurement='altura',
                            value=height, acronym='im', units='cm'),
                Measurement(name_measurement='contorno de pecho',
                            value=arr_measurements[9], acronym='c_p', units='cm'),
                Measurement(name_measurement='contorno de cintura',
                            value=arr_measurements[1], acronym='t_w_c', units='cm'),
                Measurement(name_measurement='contorno de cintura natural',
                            value=arr_measurements[22], acronym='c_c_n', units='cm'),
                Measurement(name_measurement='contorno de cadera alta',
                            value=arr_measurements[2], acronym='c_c_a', units='cm'),
                Measurement(name_measurement='contorno de cadera baja',
                            value=arr_measurements[23], acronym='c_c_b', units='cm'),
                Measurement(name_measurement='alto de talle de espalda', value=(
                    arr_measurements[18] - arr_measurements[3]), acronym='a_t_e', units='cm'),
                Measurement(name_measurement='alto de talle delantero', value=(
                    arr_measurements[18] - arr_measurements[21]), acronym='a_t_t', units='cm'),
                Measurement(name_measurement='alto de pecho',
                            value=arr_measurements[17], acronym='a_p', units='cm'),
                Measurement(name_measurement='alto de caderas alta',
                            value=arr_measurements[6], acronym='a_c_a', units='cm'),
                Measurement(name_measurement='alto de caderas baja',
                            value=arr_measurements[24], acronym='a_c_b', units='cm'),
                Measurement(name_measurement='separacion del pecho',
                            value=arr_measurements[8], acronym='s_p', units='cm'),
                Measurement(name_measurement='ancho de espalda',
                            value=arr_measurements[10], acronym='a_a', units='cm'),
                Measurement(name_measurement='ancho de busto',
                            value=arr_measurements[20], acronym='a_b', units='cm'),
                Measurement(name_measurement='contorno del cuello',
                            value=arr_measurements[7], acronym='c_c', units='cm'),
                Measurement(name_measurement='ancho de hombro',
                            value=arr_measurements[7], acronym='c_c', units='cm'),
                Measurement(name_measurement='largo de brazo',
                            value=arr_measurements[15], acronym='l_b', units='cm'),
                Measurement(name_measurement='contorno de brazo',
                            value=arr_measurements[13], acronym='c_b', units='cm'),
                Measurement(name_measurement='contorno de muñeca',
                            value=arr_measurements[14], acronym='c_m', units='cm'),
                Measurement(name_measurement='tiro al suelo',
                            value=arr_measurements[0], acronym='t_s', units='cm'),
                Measurement(name_measurement='entrepierna delantera',
                            value=arr_measurements[5], acronym='e_p_d', units='cm'),
                Measurement(name_measurement='entrepierna trasera',
                            value=arr_measurements[4], acronym='e_p_t', units='cm'),
                Measurement(name_measurement='ancho de muslo',
                            value=arr_measurements[19], acronym='a_m', units='cm'),
                Measurement(name_measurement='contorno de pantorrilla',
                            value=arr_measurements[12], acronym='c_p_ll', units='cm'),
                Measurement(name_measurement='contorno de rodilla',
                            value=arr_measurements[11], acronym='c_r', units='cm'),
            ]
        )

        inserted_id = await self.repository.insert(entity)

        model = self.mapper.map_to_body_measurements_read(inserted_id, entity)
        return model
