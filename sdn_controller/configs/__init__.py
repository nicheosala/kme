import configparser
import os


class Configuration:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read(os.path.dirname(os.path.abspath(__file__)) + '/config.ini')
        self.IP = config["GENERIC"]["IP"]
        self.PORT = int(config["GENERIC"]["PORT"])
        self.POLL_INTERVAL = float(config["GENERIC"]["POLL_INTERVAL"])


Config = Configuration()
