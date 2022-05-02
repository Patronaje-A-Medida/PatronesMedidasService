from domain.entities.body_measurements import BodyMeasurements
from domain.models.measurements.body_measurements_read import BodyMeasurementsRead


class Mapper():
    def __init__(self) -> None:
        pass

    def map_to_body_measurements_read(
            self,
            entity: BodyMeasurements) -> BodyMeasurementsRead:
        model = BodyMeasurementsRead(
            id=str(entity.id),
            client_id=entity.client_id, 
            measurement_date=entity.measurement_date, 
            measurements=entity.measurements
        )
        return model
