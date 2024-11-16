from flask import send_from_directory, request

from routes import routes_bp


@routes_bp.route('/results/download', methods=['GET'])
def download():
    pair_id = request.args["id"]
    return send_from_directory(f"static/reports/{pair_id}", "report.xlsx")
