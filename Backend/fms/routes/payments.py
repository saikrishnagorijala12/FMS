from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from fms.services import payments

payments_bp = Blueprint("payments", __name__, url_prefix="/payments")


@payments_bp.route("", methods=["POST"])
@jwt_required()
def process_payment():
    data = request.json
    user_id = get_jwt_identity()
    role = get_jwt().get("role_name")

    response, status = payments.process_payment(data, user_id, role)
    return jsonify(response), status

@payments_bp.route("", methods=["GET"])
@jwt_required()
def get_payment_history():
    user_id = get_jwt_identity()
    role = get_jwt().get("role_name")

    response, status = payments.get_payments(role, user_id)
    return jsonify(response), status

@payments_bp.route("/<int:payment_id>", methods=["GET"])
@jwt_required()
def get_payment(payment_id):
    user_id = get_jwt_identity()
    role = get_jwt().get("role_name")

    response, status = payments.get_payment_by_id(payment_id, user_id, role)
    return jsonify(response), status

@payments_bp.route("/<int:payment_id>/refund", methods=["POST"])
@jwt_required()
def refund_payment(payment_id):
    role = get_jwt().get("role_name")
    response, status = payments.process_refund(payment_id, role)
    return jsonify(response), status


@payments_bp.route("/methods", methods=["GET"])
@jwt_required()
def get_payment_methods():
    methods = [
        "Credit Card",
        "Debit Card",
        "UPI",
        "Net Banking",
        "Wallet",
        "Cash on Delivery"
    ]
    return jsonify({"payment_methods": methods}), 200
