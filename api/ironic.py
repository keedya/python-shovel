from app import api
from flask_restplus import Resource, fields
import lib.ironic_service as ironic_service

ironic_route = api.namespace('Ironic', description='Ironic Wrapper')


@ironic_route.route('/nodes')
class GetNodes(Resource):
    def get(self):
        '''List all Ironic registered nodes'''
        return ironic_service.get_node_list()


@ironic_route.route('/nodes/<string:identifier>')
class GetNode(Resource):
    def get(self, identifier):
        '''List a node in Ironic using uuid'''
        return ironic_service.get_node(identifier)


@ironic_route.route('/drivers')
class GetDriverList(Resource):
    def get(self):
        '''List node in Ironic drivers'''
        return ironic_service.get_driver_list()


@ironic_route.route('/ports')
class GetPortList(Resource):
    def get(self):
        '''List ports list in Ironic '''
        return ironic_service.get_port_list()
