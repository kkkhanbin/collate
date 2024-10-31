from dotenv import load_dotenv
load_dotenv('.env')

from flask import Flask
from flask_restful import Api

from src.config import config, add_resources, RESOURCES

# Создание приложения и его конфигурация
app = Flask(__name__)
app.config.from_object(config)

# Регистрация REST Api
api = Api(app)
add_resources(api, *RESOURCES)
