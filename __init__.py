import os
import configparser

dir_path = os.path.dirname(__file__)
config_path = os.path.join(dir_path, "config.ini")
config = configparser.RawConfigParser()	
config.read(config_path)
