import os
import configparser
import sys
from pymongo import MongoClient

config = configparser.ConfigParser()
config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), '.cfg')
config.read(config_path)

# Database access configuration settings
MONGO_URI = config['DATABASE'].get('MONGO_URI')
MONGO_DB = config['DATABASE'].get('MONGO_DB')

# if not MONGO_URI or not MONGO_DB:
#     print("MONGO_URI or MONGO_DB not specified in configuration.", file=sys.stderr)
#     sys.exit(1)

# Initialize MongoDB client and database
client = MongoClient(MONGO_URI)
db = client[MONGO_DB]

def get_database():
    return db

