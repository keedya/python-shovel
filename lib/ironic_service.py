import ironicclient
from json import loads, dumps
import json
from config.settings import config as general_config
from ironicclient.v1.node import NodeManager
from ironicclient.v1.driver import DriverManager
from ironicclient.v1.port import PortManager
from ironicclient.common.apiclient.exceptions import HTTPClientError

config = general_config['ironic']
AUTH = config

TYPES = NodeManager, DriverManager, PortManager


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, TYPES):
            return str(o)
        return loads(json.JSONEncoder.default(self, o))


def get_response(result):
    return loads(JSONEncoder().encode(result.__dict__))


def get_client():
    kwargs = AUTH
    return ironicclient.client.get_client(1, **kwargs)


def get_node_list():
    client = get_client()
    try:
        return [get_response(item)
                for item in client.node.list()], 200
    except HTTPClientError as err:
        return {'error': err.message}, err.http_status


def get_node(uuid):
    client = get_client()
    try:
        return get_response(client.node.get(uuid)), 200
    except HTTPClientError as err:
        return {'error': err.message}, err.http_status


def create_node(**kwargs):
    client = get_client()
    try:
        return get_response(client.node.create(**kwargs)), 201
    except HTTPClientError as err:
        return {'error': err.message}, err.http_status


def delete_node(uuid):
    client = get_client()
    try:
        return get_response(client.node.delete(uuid)), 202
    except HTTPClientError as err:
        return {'error': err.message}, err.http_status


def create_port(**kwargs):
    client = get_client()
    try:
        return get_response(client.port.create(**kwargs)), 201
    except HTTPClientError as err:
        return {'error': err.message}, err.http_status


def get_port_list():
    client = get_client()
    try:
        return [get_response(item)
                for item in client.port.list()], 200
    except HTTPClientError as err:
        return {'error': err.message}, err.http_status


def set_power_state(uuid, state):
    client = get_client()
    return client.node.set_power_state(uuid, state)


def get_driver_list():
    client = get_client()
    try:
        return [get_response(item)
                for item in client.driver.list()], 200
    except HTTPClientError as err:
        return {'error': err.message}, err.http_status
