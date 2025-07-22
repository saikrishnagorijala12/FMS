from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required,get_jwt
from fms.services import auth

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
@cross_origin(origins='http://localhost:4200', supports_credentials=True)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    response, status = auth.create_user(data)
    return jsonify(response), status

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    response, status = auth.login_user(data)
    return jsonify(response), status

@auth_bp.route('/refresh', methods=['POST'])
def refresh():
    data = request.json
    response, status = auth.refresh_status(data)
    return jsonify(response), status


@auth_bp.route("/auth/logout", methods=["POST"])
@jwt_required()
def logout():
    response, status = auth.logout_user()
    return jsonify(response), status
