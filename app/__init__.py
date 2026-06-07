# app/__init__.py
# This is the "app factory" — it builds and configures our Flask app.
# Having it here lets us create the app in tests too, cleanly.

from flask import Flask


def create_app():
    app = Flask(__name__)

    # Import and register our routes
    from app.routes import bp
    app.register_blueprint(bp)

    return app