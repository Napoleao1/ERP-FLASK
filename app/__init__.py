import os

from flask import Flask
from dotenv import load_dotenv
from app.extensions import db
from app.routes import web_bp

load_dotenv()


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    db.init_app(app)

    app.register_blueprint(web_bp)

    with app.app_context():
        db.create_all()

    return app