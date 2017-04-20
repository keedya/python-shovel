from app import api
from flask_restplus import Resource, fields
from lib.rackhd_service import RackHDClient


rackhd_client = RackHDClient()
rackhd_route = api.namespace('RackHD', description='RackHD Wrapper')


@rackhd_route.route('/nodes')
class GetNodes(Resource):
    '''Shows a list of all compute nodes in RackHD'''
    def get(self):
        '''List all compute nodes'''
        return rackhd_client.get_compute_nodes()


@rackhd_route.route('/nodes/<string:identifier>/catalogs')
class GetNodesCatalogs(Resource):
    '''Shows compute node catalogs in RackHD'''
    def get(self, identifier):
        '''List all compute nodes'''
        return rackhd_client.get_catalogs(identifier)


@rackhd_route.route('/nodes/<string:identifier>/catalogs/<string:source>')
class GetNodesCatalogsSource(Resource):
    '''Shows compute node catalog by source in RackHD'''
    def get(self, identifier, source):
        '''List all compute nodes'''
        return rackhd_client.get_catalogs_by_source(identifier, source)


@rackhd_route.route('/nodes/<string:identifier>/sel')
class GetNodesSel(Resource):
    '''Shows compute node sel in RackHD'''
    def get(self, identifier):
        '''List all compute nodes'''
        return rackhd_client.get_node_sel(identifier)
