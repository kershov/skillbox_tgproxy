from flask import request

from app import app
from app.helper import token_required, send_message, error_response, abort


@app.route('/api/send_message', methods=['POST'])
@token_required
def process_incoming_proxy_request():
    message = request.json.pop("message", None)

    if not message:
        return abort(400, 'Message is missing.')

    return send_message(message)


@app.errorhandler(Exception)
def handle_error(e):
    return error_response(e)
