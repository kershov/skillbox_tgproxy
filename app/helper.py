import datetime
from functools import wraps

import click
import jwt
import requests
from flask import jsonify, make_response, request, json

from app import app


def response(status, status_code, message=None):
    payload = {'ok': status}

    if message:
        payload["message"] = message

    return make_response(jsonify(payload), status_code)


def send_message(message):
    url = f"https://api.telegram.org/bot{app.config['TELEGRAM_TOKEN']}/sendMessage"

    payload = {
        'chat_id': app.config['TELEGRAM_CHAT_ID'],
        'parse_mode': 'MarkdownV2',
        'text': message
    }

    try:
        api_response = requests.post(url, json=payload)
    except requests.exceptions.ConnectionError as e:
        return response(False, 400, e.args[0].args[0])
    else:
        return make_response(api_response.json(), api_response.status_code)


def encode_auth_token(token_id, secret_key=None, expiry_days=None, algorithm=None):
    secret_key = secret_key or app.config['JWT_SECRET_KEY']
    expiry_days = expiry_days or app.config['AUTH_TOKEN_EXPIRY_DAYS']
    algorithm = algorithm or 'HS256'

    payload = {
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=expiry_days),
        'id': token_id
    }

    return jwt.encode(payload=payload, key=secret_key, algorithm=algorithm)


def decode_auth_token(token):
    try:
        payload = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms='HS256')
        return payload['id']

    except jwt.ExpiredSignatureError:
        return 'Signature expired.'

    except jwt.InvalidTokenError:
        return 'Invalid token.'

    except KeyError:
        return 'Invalid token data.'


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.json.get("token")

        if not token:
            return response(False, 401, 'Token is missing.')

        decoded_token = decode_auth_token(token)

        if decoded_token == app.config['AUTHORIZED_APP']:
            return f(*args, **kwargs)

        elif isinstance(decoded_token, str):
            message = decoded_token
            return response(False, 401, message)

    return decorated


@click.command("jwtgen", help="Generate JWT token.")
@click.option("--token-id", help="User/app/whatever id for your token.")
@click.option("--secret", help="Secret for your token.")
@click.option("--exp", default=30, help="Number of days from now your token to be expired.")
@click.option("--algorithm", help="Algorithm (default 'HS256').")
def get_jwt_token(token_id, secret, exp, algorithm):
    token = encode_auth_token(token_id, secret_key=secret, expiry_days=exp, algorithm=algorithm)
    result = {"token": token.decode("UTF-8")}
    click.echo(json.dumps(result))


app.cli.add_command(get_jwt_token)
