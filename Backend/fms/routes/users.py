from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required,get_jwt
from fms.services import users

user_bp = Blueprint('users', __name__, url_prefix='/users')

@user_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    # print("Request content type:", request.content_type)
    # print("Request data:", request.data)
    # print("Request json:", request.get_json(silent=True))
    response, status = users.get_user_profile()
    return jsonify(response), status


@user_bp.route('/profile', methods=['POST'])
@jwt_required()
def update_profile():
    data = request.json
    # print("Request content type:", request.content_type)
    # print("Request data:", request.data)
    # print("Request json:", request.get_json(silent=True))
    response, status = users.update_user_profile(data)
    return jsonify(response), status

@user_bp.route('/password', methods=['PUT'])
@jwt_required()
def change_password():
    data = request.json
    response, status = users.change_user_password(data)
    return jsonify(response), status


@user_bp.route("/users/<int:user_id>", methods=["GET"])
@jwt_required()
def get_user_details(user_id):
    response, status = users.get_requested_profile(user_id)
    return jsonify(response), status


@user_bp.route("/users/<int:user_id>/status", methods=["PUT"])
@jwt_required()
def update_user_status(user_id):
    data = request.json
    response, status = users.update_status(user_id, data)
    return jsonify(response), status
