from on_http_api2_0 import ApiApi as Api
from on_http_api2_0 import Configuration
from on_http_api2_0 import ApiClient
from config.settings import config as general_config
from on_http_api2_0.rest import ApiException
from json import loads

# tuple in functions returns
DATA = 0
STATUS = 1


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
        if (self.__client.last_response.data) is '' or None:
            return ''
        return loads(self.__client.last_response.data)

    def get_status(self):
        return self.__client.last_response.status

    def get_compute_nodes(self):
        try:
            Api().nodes_get_all()
        except ApiException as err:
            return loads(err.body), err.status
        return [item for item in self.get_response() if item.get('type') == 'compute' and
                self.is_valid_catalog(item.get('id'))]

    def get_catalogs(self, identifier):
        try:
            Api().nodes_get_catalog_by_id(identifier=identifier)
        except ApiException as err:
            return loads(err.body), err.status
        return self.get_response(), self.get_status()

    def get_catalogs_by_source(self, identifier, source):
        try:
            Api().nodes_get_catalog_source_by_id(identifier=identifier, source=source)
        except ApiException as err:
            return loads(err.body), err.status
        return self.get_response(), self.get_status()

    def get_node(self, identifier):
        try:
            Api().nodes_get_by_id(identifier=identifier)
        except ApiException as err:
            return loads(err.body), err.status
        if self.is_valid_catalog(identifier):
            return self.get_response(), self.get_status()
        else:
            return '', 204

    def get_node_sel(self, identifier):
        pollers = self.get_pollers(identifier=identifier)
        sel_id = None
        if pollers[STATUS] is not 200:
            return pollers
        for item in pollers[DATA]:
            if item['config']['command'] == 'sel':
                sel_id = item.get('id')
                break
        if sel_id is None:
            raise Exception('cannot find sel pollers for node {0}'.format(identifier))
        return self.get_poller_data(identifier=sel_id)

    def get_poller_data(self, identifier):
        try:
            Api().pollers_current_data_get(identifier=identifier)
        except ApiException as err:
            return loads(err.body), err.status
        return self.get_response(), self.get_status()

    def get_pollers(self, identifier):
        try:
            Api().nodes_get_pollers_by_id(identifier=identifier)
        except ApiException as err:
            return loads(err.body), err.status
        return self.get_response(), self.get_status()

    # only return true if dmi source and bmc is valid
    def is_valid_catalog(self, identifier):
        dmi = self.get_catalogs_by_source(identifier=identifier, source='dmi')
        if dmi[DATA].get('data') is None:
            return False
        bmc = self.get_catalogs_by_source(identifier=identifier, source='bmc')
        return (False if bmc[DATA].get('data') is None else True)

    def get_node_disk_size(self, identifier):
        local_gb = 0
        lsscsi = self.get_catalogs_by_source(identifier=identifier, source='lsscsi')
        if lsscsi[DATA].get('data') is None:
            raise Exception('lsscsi data is empty for node {0}'.format(identifier))
        for item in lsscsi.get('data'):
            if item['peripheralType'] is 'disk':
                local_gb += int(item['size'].replace('GB', '').trim())
        return local_gb

    def get_node_memory_size(self, identifier):
        dmi = self.get_catalogs_by_source(identifier=identifier, source='dmi')
        if dmi[DATA].get('data') is None:
            raise Exception('dmi data is empty for node {0}'.format(identifier))
        data = dmi.get('data')
        dmi_total = 0
        if data.get('Memory Device') is not None:
            mmemory_device = data['Memory Device']
            for item in mmemory_device:
                if item['Size'].find('GB') > 0:
                    dmi_total += int(item['Size'].replace('GB', '').trim() * 1000)
                if item['Size'].find('GB') > 0:
                    dmi_total += int(item['Size'].replace('GB', '').trim())
        return dmi_total

    def get_node_cpu(self, identifier):
        dmi = self.get_catalogs_by_source(identifier=identifier, source='dmi')
        if dmi[DATA].get('data') is None:
            raise Exception('dmi data is empty for node {0}'.format(identifier))
        data = dmi.get('data')
        if data.get('Processor Information') is not None:
            return len(data.get('Processor Information'))
        else:
            return 0
