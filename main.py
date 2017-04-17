from config.settings import config
from app import app


if __name__ == '__main__':
    app.run(host=config['shovel']['host'],
            port=config['shovel']['port'],
            debug=config['shovel']['debug'])
