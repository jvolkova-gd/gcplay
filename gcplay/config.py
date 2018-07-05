import logging
import configparser
from os import environ, getenv
from os import path
from configparser import NoOptionError, NoSectionError


CFGPATH = path.abspath("./config/conf.ini")

class Config(object):

    def __init__(self):
        self.config = configparser.ConfigParser()
        if path.isfile(CFGPATH):
            self.config.read(CFGPATH)
        else:
            print(CFGPATH)

    def get(self, section, option):
        try:
            return self.config.get(section, option)
        except(NoSectionError, NoOptionError) as e:
            logging.warning("err: %s", e)
            return None

    def init_connect(self):
        var_name = "GOOGLE_APPLICATION_CREDENTIALS"
        var_value = path.expanduser(self.get("main", var_name))
        environ[var_name] = var_value
        logging.info("ENV VAR %s set AS %s", var_name, var_value)
