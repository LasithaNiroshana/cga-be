from pymongo import MongoClient
from booking_manager.models.service_model import ServiceModel, AvailableTimeModel


class ServicesService:
    def __init__(self, db):
        self.collection = db["services"]

    # Get all services from the MongoDB collection and convert them to `ServiceModel`
    def get_all_services(self):
        services = self.collection.find()
        return [ServiceModel(**service) for service in services]

