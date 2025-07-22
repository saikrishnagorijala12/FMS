import os
import secrets
from datetime import timedelta

from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_refresh_token, create_access_token
from flask_cors import CORS


db=SQLAlchemy()
jwt = JWTManager()
cors = CORS()
jwt_blacklist = set()

from .blueprint import register_routes

def generate_secret_key():
    return secrets.token_hex(24)

def generate_jwt_key():
    return secrets.token_hex(32)

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or generate_secret_key()
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY') or generate_jwt_key()
    app.config['JWT_ALGORITHM'] = 'HS256'
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)
    app.config["JWT_BLACKLIST_ENABLED"] = True
    app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access", "refresh"]
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = (f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
                                      f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}")
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        "connect_args": {
            "options": "-c search_path=FMS2"
        }
    }
    db.init_app(app)
    jwt.init_app(app)
    register_routes(app)

    CORS(app)

    return app



@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return jti in jwt_blacklist



def generate_access_token(user):
    return create_access_token(
        identity=str(user.user_id),
        additional_claims={
            "role_id": str(user.role_id),
            "role_name": user.role.role_name,
            # "franchisor_id": str(user.franchisor.franchisor_id) if user.franchisor else None
        },
        expires_delta=timedelta(minutes=60)
    )

def refresh_access_token(user):
    return create_refresh_token(
        identity=str(user.user_id),
        additional_claims={
            "role_id": str(user.role_id),
            "role_name": user.role.role_name  # accessing via relationship
        },
        expires_delta=timedelta(minutes=60)  # or longer if needed
    )