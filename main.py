from config.settings import config
from app import app
from api.rackhd import rackhd_route
from api.ironic import ironic_route
from api.glance import glance_route
from api.shovel import shovel_route
from lib.pollers_update import sel_worker


if __name__ == '__main__':
    # Run pollers
    sel_worker.setDaemon(True)
    sel_worker.start()
    # start Rest api server
    app.run(host=config['shovel']['host'],
            port=config['shovel']['port'],
            debug=config['shovel']['debug'])

    