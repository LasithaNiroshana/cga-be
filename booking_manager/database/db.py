import os
import configparser
import sys

config = configparser.ConfigParser()
config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), '.cfg')
config.read(config_path)

# Database access configuration settings
MONGO_URI = config['DATABASE']['MONGO_URI']
MONGO_DB = config['DATABASE']['MONGO_DB']

if not config.sections():
    print("Configuration file not loaded. Check the path:", config_path, file=sys.stderr)
    sys.exit(1)

if 'DATABASE' not in config:
    print("Section 'DATABASE' not found in configuration file.", file=sys.stderr)
    sys.exit(1)

