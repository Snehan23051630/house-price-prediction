import os
from flask import Flask
from .config import config_map
from .model import load_model

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def create_app(env: str = 'default') -> Flask:
    app = Flask(
        __name__,
        template_folder=os.path.join(ROOT_DIR, 'templates'),
        static_folder=os.path.join(ROOT_DIR, 'static'),
    )

    app.config.from_object(config_map.get(env, config_map['default']))

    with app.app_context():
        app.config['MODEL'] = load_model()

    from .routes import main, auth, api
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(api)

    return app