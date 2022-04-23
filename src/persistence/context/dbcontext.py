import motor.motor_asyncio
#from bson.objectid import ObjectId

MONGO_CONNECTION_STRING = "mongodb+srv://devmardy:#Timones0819@dbpatronesymedidas.dokun.mongodb.net/DBPatronesYMedidas?retryWrites=true&w=majority"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_CONNECTION_STRING)
#database = client['DBPatronesYMedidas']

class DbContext():
    def __init__(self) -> None:
        #self.client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_CONNECTION_STRING)
        self.database = client['DBPatronesYMedidas']
        #self.body_measurements_collection = database.get_collection("BodyMeasurements")
        self.body_measurements_collection = self.database["BodyMeasurements"]

