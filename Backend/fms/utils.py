# import secrets
# from datetime import timedelta
# from fms import create_app
# from flask_jwt_extended import create_access_token, create_refresh_token, JWTManager
#
# app = create_app()
#
# jwt = JWTManager(app)
#
# jwt_blacklist = set()
#
# @jwt.token_in_blocklist_loader
# def check_if_token_revoked(jwt_header, jwt_payload):
#     jti = jwt_payload["jti"]
#     return jti in jwt_blacklist
#
#
#
# def generate_access_token(user):
#     return create_access_token(
#         identity=str(user.user_id),
#         additional_claims={"role_id": str(user.role_id)},
#         expires_delta=timedelta(minutes=30)
#     )
#
# def refresh_access_token(user):
#     return create_refresh_token(
#         identity=str(user.user_id),
#         expires_delta=timedelta(minutes=30)  # long expiry
#     )

from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from fms.models.Notification import Notification
from fms import db

def notify(user_id, message):
    db.session.add(Notification(user_id=user_id, message=message))
    db.session.commit()

def role_required(role):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims.get('role') != role:
                return {'msg': 'Access denied'}, 403
            return f(*args, **kwargs)
        return wrapper
    return decorator

