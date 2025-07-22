import fms.utils as utils
from fms import jwt_blacklist,jwt
from flask_jwt_extended import get_jwt_identity, get_jwt
from werkzeug.security import generate_password_hash, check_password_hash
from fms import db
from fms.models.User import User


def get_user_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return {'error': 'User not found'}, 404

    return {
        'user_id': user.user_id,
        'name': user.name,
        'email': user.email,
        'phone_no': str(user.phone_no),
        'role_id': user.role_id
    }, 200
    # identity = get_jwt_identity()
    # print(identity)
    # user = User.query.get(identity['user_id'])
    # if not user:
    #     return {'error': 'User not found'}, 404
    #
    # return {
    #     'user_id': user.user_id,
    #     'name': user.name,
    #     'email': user.email,
    #     'phone_no': str(user.phone_no),
    #     'role_id': user.role_id
    # }, 200


def update_user_profile(data):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return {'error': 'User not found'}, 404

    user.name = data.get('name', user.name)
    user.phone_no = data.get('phone_no', user.phone_no)
    user.role_id = data.get('role_id', user.role_id)
    db.session.commit()
    return {'message': 'Profile updated'}, 200


def change_user_password(data):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return {'error': 'User not found'}, 404
    if not check_password_hash(user.password, data['old_password']):
        return {'error': 'Old password is incorrect'}, 403
    user.password = generate_password_hash(data['new_password'])
    db.session.commit()
    return {'message': 'Password changed'}, 200


def get_requested_profile(user_id):
    claims = get_jwt()

    # Check if the user is admin (role_id = 1)
    if str(claims.get("role_id")) != "1":
        return {"error": "Admins only"}, 403

    user = User.query.get(user_id)
    if not user:
        return {"error": "User not found"}, 404

    return {
        "user_id": user.user_id,
        "email": user.email,
        "name": user.name,
        "role_id": user.role_id,
        # add any other fields you want to expose
    }, 200


def update_status(user_id,data):
    claims = get_jwt()

    # Only Admins (role_id == 1) allowed
    if str(claims.get("role_id")) != "1":
        return {"error": "Admins only"}, 403


    if "is_active" not in data:
        return {"error": "Missing 'is_active' in payload"}, 400

    user = User.query.get(user_id)
    if not user:
        return {"error": "User not found"}, 404

    user.is_active = data["is_active"]
    db.session.commit()

    return {"message": f"User {'activated' if user.is_active else 'deactivated'} successfully."}, 200