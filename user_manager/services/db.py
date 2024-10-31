import os
import configparser

config = configparser.ConfigParser()
config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'cfg')
config.read(config_path)

# Access configuration settings
MONGO_URI = config['DATABASE']['MONGO_URI']
MONGO_DB = config['DATABASE']['MONGO_DB']