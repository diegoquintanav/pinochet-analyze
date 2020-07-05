# services/users/project/config.py

import os


class BaseConfig:
    """Base configuration"""

    TESTING = False
    SECRET_KEY = os.environ.get("SECRET_KEY")

    BIND_HOST = os.environ.get('BIND_HOST', default='127.0.0.1')
    BIND_PORT = os.environ.get('BIND_PORT', default=5000)
    NEO4J_HOST = os.environ.get('NEO4J_HOST', default='localhost')
    NEO4J_PORT = os.environ.get('NEO4J_PORT', default=7687)


class DevelopmentConfig(BaseConfig):
    """Development configuration"""

    DEBUG = True
    NEO4J_USER = os.environ.get('NEO4J_USER', default='neo4j')
    NEO4J_PASSWORD = os.environ.get('NEO4J_PASSWORD', default='admin')


class TestingConfig(BaseConfig):
    """Testing configuration"""

    TESTING = True
    NEO4J_USER = os.environ.get('NEO4J_USER', default='neo4j')
    NEO4J_PASSWORD = os.environ.get('NEO4J_PASSWORD', default='admin')


class ProductionConfig(BaseConfig):
    """Production configuration"""

    DEBUG = False
    NEO4J_USER = os.environ.get('NEO4J_USER')
    NEO4J_PASSWORD = os.environ.get('NEO4J_PASSWORD')
