from flask import Flask, escape, request, json
from flask_sslify import SSLify
import os
import requests

app = Flask(__name__)
sslify = SSLify(app)

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')


def send_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "parse_mode": "MarkdownV2",
        "text": message
    }

    try:
        response = requests.post(url, json=payload)
    except Exception as e:
        print(e)
    else:
        return response.status_code, response.content


@app.errorhandler(405)
def method_not_allowed(e):
    return app.response_class(response=json.dumps({"ok": False}), mimetype='application/json', status=405)


@app.route('/', methods=['GET', 'POST'])
def process_incoming_proxy_request():
    if request.method == 'POST':
        message = request.args.get("text", "World")
        message = escape(message)

        return f'Hello, {send_message(message)}!'
    else:
        return "Hello!"


if __name__ == '__main__':
    app.run(debug=True)
