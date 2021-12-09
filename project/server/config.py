# project/server/config.py

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    """Base configuration."""

    APP_NAME = os.getenv("APP_NAME", "reconciliation")
    SECRET_KEY = os.getenv("SECRET_KEY", "my_precious")
    WTF_CSRF_ENABLED = False


class DevelopmentConfig(BaseConfig):
    """Development configuration."""

    TESTING = False


class TestingConfig(BaseConfig):
    """Testing configuration."""
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    TESTING = True


class ProductionConfig(BaseConfig):
    """Production configuration."""
    WTF_CSRF_ENABLED = True
