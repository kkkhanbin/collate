import os
import sys
sys.path.append(os.path.abspath('..'))

from waitress import serve

from dotenv import load_dotenv
load_dotenv('.env')

from flask import Flask

from config import config, BLUEPRINTS, register_blueprints

# Создание приложения и его конфигурация
app = Flask(__name__)
app.config.from_object(config)

# Регистрация Blueprint`ов
register_blueprints(app, *BLUEPRINTS)


def main():
    port = os.getenv('PORT')
    if port is None:
        serve(app, host='0.0.0.0', port=5000)
    else:
        serve(app, host='0.0.0.0', port=int(port))


if __name__ == '__main__':
    main()
