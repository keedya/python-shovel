from app import api
from flask_restplus import Resource, fields
import lib.shovel_service as shovel_service

shovel_route = api.namespace('Shovel',
                             description='Shovel to register and unregister \
                             a compute node from RackHD with Ironic')

# models
register_model = api.model('Register', {
                           'uuid': fields.String(required=True, description='rackhd node id'),
                           'driver': fields.String(required=True, description='ironic driver'),
                           'ipmihost': fields.String(required=False),
                           'ipmiuser': fields.String(required=False),
                           'ipmipass': fields.String(required=False),
                           'name': fields.String(required=True, description='node name'),
                           'kernel': fields.String(required=True),
                           'ramdisk': fields.String(required=True),
                           'port': fields.String(required=True)})


@shovel_route.route('/register')
class register(Resource):
    @shovel_route.expect(register_model)
    def post(self):
        '''register RackHd node with Ironic'''
        return shovel_service.register(api.payload)


@shovel_route.route('/unregister/<string:uuid>')
class unregister(Resource):
    def delete(self, uuid):
        '''unregister RackHd node with Ironic'''
        return shovel_service.unregister(uuid)
