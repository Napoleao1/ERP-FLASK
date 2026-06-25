import os

from flask import Flask # type: ignore
from dotenv import load_dotenv
from app.extensions import db, cors
from app.routes import web_bp, api_bp

load_dotenv()


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    db.init_app(app)


    origens_permitidas = os.getenv("CORS_ORIGINS").split(",")
    
    cors.init_app(app, resources={
        r"/api/*":
            {
                "origins": origens_permitidas
            }
        
    })
    
    app.register_blueprint(web_bp)
    app.register_blueprint(api_bp)


    with app.app_context():
        db.create_all()

    return app