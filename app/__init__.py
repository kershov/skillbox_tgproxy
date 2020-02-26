import os
from flask import Flask
from flask_sslify import SSLify

# Initialize application
app = Flask(__name__, static_folder=None)
sslify = SSLify(app)

# App configuration
app_settings = os.getenv(
    'APP_SETTINGS',
    'app.config.ProductionConfig'
)
app.config.from_object(app_settings)

# Import the application views
from app import views
