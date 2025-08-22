from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required,get_jwt
from fms.services import  franchises as f

franchises_bp = Blueprint('franchises', __name__, url_prefix='/franchises')

@franchises_bp.route('/apply', methods=['POST'])
@jwt_required()
def apply_for_franchise():
    data = request.json
    response, status = f.apply_franchise(data)
    return jsonify(response), status

@franchises_bp.route('/applications/<int:application_id>/reject', methods=['PUT'])
@jwt_required()
def reject_application(application_id):
    claims = get_jwt()
    if claims.get("role_name") != "Franchisor":
        return jsonify({"msg": "Unauthorized"}), 403
    return f.update_application_status(application_id, approved=False)

# Get all franchises
@franchises_bp.route('', methods=['GET'])
@jwt_required()
def get_all_franchises():
    return f.get_all_franchises()

# Get specific franchise details
@franchises_bp.route('/<int:franchise_id>', methods=['GET'])
@jwt_required()
def get_franchise(franchise_id):
    return f.get_franchise_by_id(franchise_id)

# Update franchise details
@franchises_bp.route('/<int:franchise_id>', methods=['PUT'])
@jwt_required()
def update_franchise(franchise_id):
    data = request.json
    return f.update_franchise(franchise_id, data)

# Update franchise Application status
@franchises_bp.route('/<int:application_id>/status', methods=['PUT'])
@jwt_required()
def update_franchise_status(application_id):
    data = request.json
    return f.update_status(application_id, data)

# Get franchisee's own franchise
@franchises_bp.route('/my-franchise', methods=['GET'])
@jwt_required()
def get_my_franchise():
    claims = get_jwt()
    user_id = claims.get("user_id")
    return f.get_franchise_by_user(user_id)