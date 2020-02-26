from app import app
from flask import jsonify, make_response
import requests


def response(status, status_code):
    return make_response(jsonify({'ok': status})), status_code


def send_message(message):
    url = f"https://api.telegram.org/bot{app.config.get('TELEGRAM_TOKEN')}/sendMessage"
    payload = {
        "chat_id": app.config.get('TELEGRAM_CHAT_ID'),
        "parse_mode": "MarkdownV2",
        "text": message
    }

    try:
        api_response = requests.post(url, json=payload)
    except Exception:
        return response(False, 400)

    return api_response
