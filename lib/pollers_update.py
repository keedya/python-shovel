from  modules.amqp import AmqpWorker
import lib.ironic_service as ironic_service
from json import loads

# tuple in functions returns
DATA = 0
STATUS = 1

def amqp_callback(ch, method, properties, body):
    print ('methodh.routingkey {0}, body {1}'.format(method.routing_key, body))
    # break point

    

sel_worker = AmqpWorker(
            exchange_name="on.events", topic_routing_key="polleralert.sel.#",
            external_callback=amqp_callback, timeout=0)
