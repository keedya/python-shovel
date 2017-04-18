import logging
import yaml

# Global logger setup: CRITICAL < ERROR < WARNING < INFO < DEBUG
LOGFORMAT = '%(asctime)s:%(name)s:%(levelname)s - %(message)s'
LOGLEVELS = {
    'CRITICAL': logging.CRITICAL,
    'ERROR': logging.ERROR,
    'WARNING': logging.WARNING,
    'INFO': logging.INFO,
    'DEBUG': logging.DEBUG
}

# default config
config = {
    'shovel': {
        'host': '0.0.0.0',
        'port': 9005,
        'debug': True,
        'logLevel': 'INFO'
    },
    'rackhd': {
        'host': 'http://localhost',
        'port': 8080,
        'api': 'api/2.0',
        'debug': False,
        'verify_ssl': False
    }
}

try:
    with open("config/config.yml", 'r') as ymlfile:
        config = yaml.load(ymlfile)
except Exception as err:
    print ('failed to read config file: {0}'.format(err))

logging.basicConfig(level=LOGLEVELS[config['shovel']['logLevel']], format=LOGFORMAT)
