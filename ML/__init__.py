import os
from flask import Flask
from .config import config_map
from .model import load_model

# Absolute path to the project root (one level up from this app/ folder)
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def create_app(env: str = 'default') -> Flask:
    """
    Application factory.

    Usage:
        app = create_app('development')   # local dev
        app = create_app('production')    # Render / Railway

    The factory pattern makes the app easy to test (pass 'testing')
    and avoids module-level side effects.
    """
    app = Flask(
        __name__,
        template_folder=os.path.join(ROOT_DIR, 'templates'),
        static_folder=os.path.join(ROOT_DIR, 'static'),
    )

    # ── Load config ───────────────────────────────────────────────────────────
    app.config.from_object(config_map.get(env, config_map['default']))

    # ── Load ML model once and store on app.config ────────────────────────────
    with app.app_context():
        app.config['MODEL'] = load_model()

    # ── Register blueprints ───────────────────────────────────────────────────
    from .routes import main, auth, api
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(api)

    return app