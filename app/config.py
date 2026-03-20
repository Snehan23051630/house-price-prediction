import os

# Absolute path to project root — works on Windows and Linux
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Config:
    """Base configuration shared by all environments."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-change-in-production')
    MODEL_PATH = os.path.join(_ROOT, 'ml', 'model.pkl')
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

class TestingConfig(Config):
    TESTING = True
    MODEL_PATH = os.path.join(_ROOT, 'ml', 'model.pkl')

# Map string names → config classes (used in __init__.py)
config_map = {
    'development': DevelopmentConfig,
    'production':  ProductionConfig,
    'testing':     TestingConfig,
    'default':     DevelopmentConfig,
}