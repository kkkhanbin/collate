import os
import sys
sys.path.append(os.path.abspath('..'))

from waitress import serve

from dotenv import load_dotenv
load_dotenv('.env')

from flask import Flask
from flask_restful import Api

from config import config, add_resources, RESOURCES

# Создание приложения и его конфигурация
app = Flask(__name__)
app.config.from_object(config)

# Регистрация REST Api
api = Api(app)
add_resources(api, *RESOURCES)


# temporary
@app.route("/")
def successfully_deployed():
    return "Deployed" 


def main():
    port = os.getenv("PORT")
    if port is None:
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        app.run(host='0.0.0.0', port=int(port), debug=True)

    # serve(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
