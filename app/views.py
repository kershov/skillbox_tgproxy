from flask import request

from app import app
from app.helper import response, token_required, send_message


@app.errorhandler(404)
def resource_not_found(e):
    return response(False, 404, "Resource not found.")


@app.errorhandler(405)
def method_not_allowed(e):
    return response(False, 405, "Method not allowed.")


@token_required
@app.route('/api/send_message', methods=['POST'])
def process_incoming_proxy_request():
    message = request.json.get("message")

    if not message:
        return response(False, 403, "Message is missing.")

    return send_message(message)
