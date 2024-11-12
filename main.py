from fastapi import FastAPI,HTTPException
import os
import configparser
from pymongo import MongoClient
from booking_manager.routes.booking_manager_router import booking_manager_router
from user_manager.routes.user_main_router import user_manager_router

app=FastAPI(
    responses={404: {'message': 'Router not found.!'}},
    title="CGA APIs"
)

config = configparser.ConfigParser()
config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.', '.cfg')
config.read(config_path)

# Access configuration settings
MONGO_URI = config['DATABASE']['MONGO_URI']
MONGO_DB = config['DATABASE']['MONGO_DB']

client=MongoClient(MONGO_URI)

app.include_router(booking_manager_router)
app.include_router(user_manager_router)

# @app.get("/test-mongodb-connection")
# async def test_mongodb_connection():
#     try:
#         # Attempt to access the server
#         client.admin.command("ping")
#         return {"message": "Connected to MongoDB"}
#     except ConnectionError:
#         raise HTTPException(status_code=500, detail="Could not connect to MongoDB")
#
# @app.get("/")
# def read_root():
#     return {"Hello": "World"}

