import logging
import configparser
from os import environ, getenv
from os import path
from configparser import NoOptionError, NoSectionError
from google.cloud import bigquery

CONFIG_PATH = path.abspath("./config/conf.ini")
CREDENTIALS_NAME = "GOOGLE_APPLICATION_CREDENTIALS"

logger = logging
logger.basicConfig(level=logging.DEBUG)

class Config(object):

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read(CONFIG_PATH)

    def get(self, section, option):
        try:
            return self.config.get(section, option)
        except(NoSectionError, NoOptionError) as e:
            logger.warning("err: %s", e)
            return None

    def init_connect(self):
        if not getenv(CREDENTIALS_NAME):
            var_value = path.expanduser(self.get("main", CREDENTIALS_NAME))
            environ[CREDENTIALS_NAME] = var_value
            logger.info("ENV VAR %s set AS %s", CREDENTIALS_NAME, var_value)


class BQClient(bigquery.Client):
    def __init__(self):
        if not getenv(CREDENTIALS_NAME):
            Config().init_connect()
        bigquery.Client.__init__(self)
