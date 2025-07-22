from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required,get_jwt
from fms.services import  franchise_location as locations

franchise_location_bp = Blueprint('franchise-locations', __name__, url_prefix='/franchise-locations')

@franchise_location_bp.route('/', methods=['POST'])
@jwt_required()
def post_franchise_location():
    data = request.get_json()
    response, status = locations.create_franchise_location(data)
    return jsonify(response), status

@franchise_location_bp.route('', methods=['GET'])
@jwt_required()
def get_all_locations():
    response, status = locations.fetch_franchise_location()
    return jsonify(response), status

@franchise_location_bp.route('/<int:location_id>', methods=['PUT'])
@jwt_required()
def put_location(location_id):
    data = request.get_json()
    response, status = locations.update_franchise_location(data,location_id)
    return jsonify(response), status

@franchise_location_bp.route('/<int:location_id>', methods=['DELETE'])
@jwt_required()
def delete_location(location_id):
    response, status = locations.delete_franchise_location(location_id)
    return jsonify(response), status