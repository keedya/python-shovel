from on_http_api2_0 import ApiApi as Api
from on_http_api2_0 import Configuration
from on_http_api2_0 import ApiClient
from config.settings import config as general_config
from json import loads


class RackHDClient():

    def __init__(self):
        rackhd_config = Configuration()
        config = general_config.get('rackhd')
        rackhd_config.host = config['host'] + ':' + str(config['port']) + '/' + config['api']
        rackhd_config.verify_ssl = config['verify_ssl']
        rackhd_config.api_client = ApiClient(host=rackhd_config.host)
        rackhd_config.debug = config['debug']
        self.__client = rackhd_config.api_client

    def get_response(self):
        return loads(self.__client.last_response.data)

    def get_compute_nodes(self):
        Api().nodes_get_all()
        return [item for item in self.get_response() if item.get('type') == 'compute']
