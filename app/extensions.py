from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager
from flasgger import Swagger


db = SQLAlchemy()
cors = CORS()
login_manager = LoginManager()
swagger = Swagger()
