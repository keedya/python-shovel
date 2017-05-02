from  modules.amqp import AmqpWorker
import lib.ironic_service as ironic_service
from json import loads
from lib.rackhd_service import RackHDClient

# tuple in functions returns
DATA = 0
STATUS = 1

def amqp_callback(ch, method, properties, body):
    # print ('body {1}'.format(method.routing_key, body))
    # break point
    body = loads(body)
    nodes = ironic_service.get_node_list()[DATA]
    for node in nodes:
        if node.get('extra'):
            # check if node id is a match
            if body.get('nodeId') == node['extra']['nodeid']:
               node_sel = RackHDClient().get_node_sel(node['extra']['nodeid'])[DATA][0]['sel']
               extra = node.get('extra')
               readings = body['data']['alert']['reading']
               extra['events'] = {
                   'logId': readings['SEL Record ID'],
                   'value': readings['Event Direction'],
                   'sensorType': readings['Sensor Type'],
                   'sensorNumber': readings['Sensor Number'],
                   'time': readings['Timestamp'].split(' ')[1],
                   'date': readings['Timestamp'].split(' ')[0],
                   'event': readings['Description']
               }
               data = [
                        {
                            'path': '/extra',
                            'value': extra,
                            'op': 'replace'
                        }
               ]
               if readings['Description'] == node['extra']['eventre']:
                   extra['eventcnt'] = 'SEL Error Detected'
                   ironic_service.patch_node(node.get('uuid'), data)
               break    

sel_worker = AmqpWorker(
            exchange_name="on.events", topic_routing_key="polleralert.sel.#",
            external_callback=amqp_callback, timeout=0)
