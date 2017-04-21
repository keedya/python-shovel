from config.settings import config
from app import app
from api.rackhd import rackhd_route
from api.ironic import ironic_route
from api.glance import glance_route


if __name__ == '__main__':
    app.run(host=config['shovel']['host'],
            port=config['shovel']['port'],
            debug=config['shovel']['debug'])
