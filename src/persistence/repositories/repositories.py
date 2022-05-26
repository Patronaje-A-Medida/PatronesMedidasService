from typing import List
from fastapi import Depends
from numpy import true_divide
from persistence.context.dbcontext import DbContext
from domain.entities.body_measurements import BodyMeasurements


class BodyMeasurementsRepository():
    def __init__(self, context: DbContext = Depends(DbContext)) -> None:
        self.context = context
    
    async def get_all(self) -> list:
        docs = []
        cursor = self.context.body_measurements_collection.find({})
        for doc in await cursor.to_list(length=100):
            docs.append(BodyMeasurements.from_map(doc))
        return docs

    async def insert(self, entity: BodyMeasurements) -> str:
        result = await self.context.body_measurements_collection.insert_one(entity.to_map())
        if result is not None:
            return result.inserted_id
        else:
            return None

    async def get_last_measurements(self, client_id) -> BodyMeasurements:
        docs = []
        cursor = self.context.body_measurements_collection.find({'client_id': {'$eq':client_id}})
        
        for doc in await cursor.to_list(length=100):
            docs.append(BodyMeasurements.from_map(doc))
        
        if len(docs) < 1: return None
        
        docs.sort(key=lambda x: x.measurement_date, reverse=True)
        return docs[0]

    def doc_helper(self, doc) -> dict:
        return {
            "_id": str(doc["_id"]),
            "client_id": doc["client_id"],
            "measurement_date": doc["measurement_date"],
            "measurements": doc["measurements"]
        }
