from flask import Flask
from flask_restplus import Api

app = Flask(__name__)
api = Api(app, version='1.0', title='shovel API',
          description='RackHD and OpenStack Coordinator')
