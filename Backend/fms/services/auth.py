import fms as utils
from fms import jwt_blacklist,jwt
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt
from werkzeug.security import generate_password_hash, check_password_hash
from fms import db
from fms.models.User import User

def create_user(data):
    if User.query.filter_by(email=data['email']).first():
        return {'error': 'Email already exists'}, 409
    user = User(
        # user_id=data['user-id'],
        name=data['name'],
        email=data['email'],
        password=generate_password_hash(data['password']),
        phone_no=data['phone_no'],
        role_id=data['role_id']
    )
    db.session.add(user)
    db.session.commit()

    return {'message': 'User created successfully'}, 201


def login_user(data):
    user = User.query.filter_by(email=data['email']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return {'error': 'Invalid credentials'}, 401

    token = utils.generate_access_token(user)

    return {'access_token': token}, 200

def refresh_status(data):
    user = User.query.filter_by(email=data['email']).first()
    if not user or not check_password_hash(user.password, data['password']):
         return {'error': 'Invalid credentials'}, 401
    token = utils.refresh_access_token(user)

    return {'new_access_token': token}, 200

def logout_user():
    jti = get_jwt()["jti"]  # unique token ID
    jwt_blacklist.add(jti)
    return {"}Successfully logged out"}, 200