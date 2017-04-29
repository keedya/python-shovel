import pika
import threading
class AmqpWorker(threading.Thread):
    def __init__(self, exchange_name, topic_routing_key, external_callback, timeout=-1):
        threading.Thread.__init__(self)
        print('amqp constructor')
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost',
                                                                            port=5672))
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(exclusive=True)
        queue_name = result.method.queue
        self.channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=topic_routing_key)
        # self.connection.add_timeout(timeout, self.dispose)
        self.channel.basic_consume(external_callback, queue=queue_name)
        print('done constructing')

    def dispose(self):
        print ('Pika connection timeout')
        if self.connection.is_closed is False:
            self.channel.stop_consuming()
            print ("Attempting to close the Pika connection")
            self.thread_stop = True

    def run(self):
        print ('start consuming')
        self.channel.start_consuming()