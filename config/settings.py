import logging
import yaml
from on_http_api2_0 import Configuration
from on_http_api2_0 import ApiClient


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
    },
    'ironic': {
        'os_username': 'admin',
        'os_password': 'password',
        'os_auth_url': 'localhost:5000/v2.0',
        'os_tenant_name': 'admin',
        'insecure': False
    },
    'glance': {
        'os_username': 'admin',
        'os_password': 'password',
        'os_auth_url': 'localhost:5000/v2.0',
        'glance_url': 'http://localhost:9292',
        'os_tenant_name': 'admin',
        'insecure': False
    }
}

try:
    with open("config/config.yml", 'r') as ymlfile:
        config = yaml.load(ymlfile)
except Exception as err:
    print ('failed to read config file: {0}'.format(err))

logging.basicConfig(level=LOGLEVELS[config['shovel']['logLevel']], format=LOGFORMAT)

# RackHD

rackhd = config['rackhd']
rackhd_config = Configuration()
rackhd_config.host = rackhd['host'] + ':' + str(rackhd['port']) + '/' + rackhd['api']
rackhd_config.verify_ssl = rackhd['verify_ssl']
rackhd_config.api_client = ApiClient(host=rackhd_config.host)
rackhd_config.debug = rackhd['debug']



