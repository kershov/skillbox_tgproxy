import os


class BaseConfig:
    """
    Base application configuration
    """
    DEBUG = False
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    AUTHORIZED_APP = os.getenv('AUTHORIZED_APP')
    AUTH_TOKEN_EXPIRY_DAYS = 3650


class DevelopmentConfig(BaseConfig):
    """
    Development application configuration
    """
    DEBUG = True


class ProductionConfig(BaseConfig):
    """
    Production application configuration
    """
    DEBUG = True

