from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from fms import db
from fms.models import CustomerPreferences
from fms.services import  customer_preferences

preferences_bp = Blueprint('preferences', __name__, url_prefix='/preferences')

@preferences_bp.route('/<int:customer_id>', methods=['GET'])
@jwt_required()
def get_preferences(customer_id):
    response, status = customer_preferences.fetch_prefernce(customer_id)
    return jsonify(response), status



@preferences_bp.route('/<int:customer_id>', methods=['POST', 'PUT'])
@jwt_required()
def set_preferences(customer_id):
    data = request.get_json()
    response, status = customer_preferences.update_preference(customer_id, data)
    return jsonify(response), status



