from app import api
from flask_restplus import Resource
from lib.rackhd_service import RackHDClient


rackhd_client = RackHDClient()
rackhd_route = api.namespace('RackHD', description='RackHD Wrapper')


@rackhd_route.route('/nodes')
class GetNodes(Resource):
    '''Shows a list of all compute nodes in RackHD'''
    def get(self):
        '''List all compute nodes'''
        return rackhd_client.get_compute_nodes()
