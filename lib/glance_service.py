import glanceclient
from json import loads, dumps
import json
from config.settings import config as general_config
from glanceclient.v1.images import ImageManager
from keystoneauth1 import loading
from keystoneauth1 import session as Session

config = general_config['glance']
TYPES = ImageManager

# Setup auth with keystone
loader = loading.get_plugin_loader('password')
auth = loader.load_from_options(
    auth_url=config['os_auth_url'],
    username=config['os_username'],
    password=config['os_password'])


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, TYPES):
            return str(o)
        return loads(json.JSONEncoder.default(self, o))


def get_response(result):
    return loads(JSONEncoder().encode(result.__dict__))


def get_client():
    session = Session.Session(auth=auth)
    return glanceclient.Client(2, config['glance_url'], token=(session).get_token(),
                               insecure=False)


def get_image_list(**kwargs):
    client = get_client()
    return [get_response(item)['__original__'] for item in client.images.list()]
