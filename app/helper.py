import datetime
from functools import wraps

import jwt
import requests
from flask import jsonify, make_response, request

from app import app


def response(status, status_code, message=None):
    payload = {'ok': status}

    if message:
        payload["message"] = message

    return make_response(jsonify(payload), status_code)


def send_message(message):
    url = f"https://api.telegram.org/bot{app.config['TELEGRAM_TOKEN']}/sendMessage"

    payload = {
        "chat_id": app.config['TELEGRAM_CHAT_ID'],
        "parse_mode": "MarkdownV2",
        "text": message
    }

    try:
        api_response = requests.post(url, json=payload)
    except requests.exceptions.ConnectionError as e:
        return response(False, 400, e.args[0].args[0])
    else:
        return make_response(api_response.json(), api_response.status_code)


def encode_auth_token(user_id):
    try:
        payload = {
            'iat': datetime.datetime.utcnow(),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=app.config['AUTH_TOKEN_EXPIRY_DAYS']),
            'sub': user_id
        }

        return jwt.encode(
            payload,
            app.config['JWT_SECRET_KEY'],
            algorithm='HS256'
        )

    except Exception as e:
        return e


def decode_auth_token(token):
    try:
        payload = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms='HS256')
        return payload['sub']

    except jwt.ExpiredSignatureError:
        return response(False, 403, 'Signature expired.')

    except jwt.InvalidTokenError:
        return response(False, 403, 'Invalid token.')


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.json.get("token")

        if not token:
            return response(False, 403, 'Token is missing.')

        decoded_token = decode_auth_token(token)

        return f(*args, **kwargs) if decoded_token == app.config['AUTHORIZED_APP'] else decoded_token

    return decorated
