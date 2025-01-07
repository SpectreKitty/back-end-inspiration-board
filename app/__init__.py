from flask import Flask
from flask_cors import CORS
import os
from .models import board, card
from .db import db, migrate
from .routes.card_routes import bp as cards_bp
from .routes.board_routes import bp as boards_bp


def create_app(config=None):
    app = Flask(__name__)
    CORS(app, origins=[
        "https://spectrekitty.github.io"
    ])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')

    if config:
        app.config.update(config)

    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints 
    app.register_blueprint(boards_bp)
    app.register_blueprint(cards_bp)

    return app
