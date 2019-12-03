import os
dir_path = os.path.dirname(__file__)
config_path = os.path.join(dir_path, "config.ini")

# for python2 and python3
try:
	import configparser
	config = configparser.RawConfigParser()
except ImportError:
	import ConfigParser
	config = ConfigParser.RawConfigParser()
config.read(config_path)
