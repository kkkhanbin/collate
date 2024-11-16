from flask import send_from_directory

from routes import routes_bp


@routes_bp.route('/favicon.ico')
def favicon():
    return send_from_directory(
        'static', 'img/favicon.ico', mimetype='img/favicon.ico')
