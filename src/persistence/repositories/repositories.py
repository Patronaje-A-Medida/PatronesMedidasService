from fastapi import Depends
from persistence.context.dbcontext import DbContext


class BodyMeasurementsRepository():
    def __init__(self, context: DbContext = Depends(DbContext)) -> None:
        self.context = context
    
    async def get_all(self) -> list:
        docs = []
        cursor = self.context.body_measurements_collection.find({})
        for doc in await cursor.to_list(length=100):
            docs.append(self.json_helper(doc))
        return docs

    def json_helper(self, doc) -> dict:
        return {
            "_id": str(doc["_id"]),
            "client_id": doc["client_id"],
            "measurement_date": doc["measurement_date"],
        }
