from app import api
from flask_restplus import Resource, fields
import lib.glance_service as glance_service

glance_route = api.namespace('Glance', description='Glance Wrapper')


@glance_route.route('/images')
class GetImages(Resource):
    def get(self):
        '''List glance images'''
        return glance_service.get_image_list()
