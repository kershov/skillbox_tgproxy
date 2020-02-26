import os


class BaseConfig:
    """
    Base application configuration
    """
    DEBUG = False
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_strong_key')
    AUTH_TOKEN_EXPIRY_DAYS = 30
    AUTH_TOKEN_EXPIRY_SECONDS = 3000


class DevelopmentConfig(BaseConfig):
    """
    Development application configuration
    """
    DEBUG = True
    AUTH_TOKEN_EXPIRY_DAYS = 1
    AUTH_TOKEN_EXPIRY_SECONDS = 20


class ProductionConfig(BaseConfig):
    """
    Production application configuration
    """
    DEBUG = True
    AUTH_TOKEN_EXPIRY_DAYS = 30
    AUTH_TOKEN_EXPIRY_SECONDS = 20
