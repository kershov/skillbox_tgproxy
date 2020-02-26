from app import app
from app.helper import send_message, response
from flask import request, escape, make_response


@app.errorhandler(405)
def method_not_allowed(e):
    return response(False, 405)


@app.route('/', methods=['GET', 'POST'])
def process_incoming_proxy_request():
    if request.method == 'POST':
        message = request.args.get("text", "World")
        message = escape(message)

        return f'Hello, {send_message(message)}!'
    else:
        resp = send_message("Test!!!")
        return make_response(resp.json(), resp.status_code)
