import os

from flask import Flask, jsonify, request # type: ignore
from werkzeug.exceptions import HTTPException
from dotenv import load_dotenv
from app.extensions import db, cors, login_manager, swagger
from app.routes import web_bp, api_bp

load_dotenv()


SWAGGER_CONFIG_OVERRIDES = {
    "title": "ERP Flask API",
    "uiversion": 3,
    "specs_route": "/apidocs/",
}

SWAGGER_TEMPLATE = {
    "info": {
        "title": "ERP Flask API",
        "description": "Documentação da API do ERP (produtos, categorias e usuários).",
        "version": "1.0.0",
    }
}


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    db.init_app(app)

    swagger.config.update(SWAGGER_CONFIG_OVERRIDES)
    swagger.template = SWAGGER_TEMPLATE
    swagger.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = "web.login_view"
    login_manager.login_message = "Você precisa estar logado para acessar esta página."
    login_manager.login_message_category = "warning"

    from app.models import Usuario

    @login_manager.user_loader
    def carregar_usuario(user_id):
        return Usuario.query.get(int(user_id))

    origens_permitidas = os.getenv("CORS_ORIGINS").split(",")
    
    cors.init_app(app, resources={
        r"/api/*":
            {
                "origins": origens_permitidas
            }
        
    })
    
    app.register_blueprint(web_bp)
    app.register_blueprint(api_bp)

    @app.errorhandler(HTTPException)
    def tratar_erro_http(e):
        if request.path.startswith("/api"):
            return jsonify({"erro": e.description, "status": e.code}), e.code
        return e

    with app.app_context():
        db.create_all()

    return app