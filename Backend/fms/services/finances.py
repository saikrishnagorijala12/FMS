from flask_jwt_extended import get_jwt, get_jwt_identity

from fms.models.Commission import Commission
from fms.models.User import User
from fms.models.Franchisee import Franchisee
from fms.models.Status import Status
from fms.models.Withdrawal import Withdrawal
from fms import db
from datetime import datetime, UTC
from sqlalchemy import func

def get_commissions(user_id, role_name):
    if role_name == "Franchisor" or role_name == "Admin":
        commissions = Commission.query.all()
    elif role_name == "Franchisee":
        franchisee = Franchisee.query.filter_by(user_id=user_id).first()
        if not franchisee:
            return {"msg": "Franchisee not found"}, 404
        commissions = Commission.query.filter_by(franchisee_id=franchisee.franchisee_id).all()
    else:
        return {"msg": "Unauthorized access"}, 403

    result = []
    for c in commissions:
        result.append({
            "commission_id": c.commission_id,
            "order_id": c.order_id,
            "franchisee_id": c.franchisee_id,
            "franchisee_name": c.franchisee.user.full_name,
            "amount": float(c.amount),
            "status": c.status.status_name,
            "created_time": c.created_time.isoformat()
        })

    return {"commissions": result}, 200


def get_earnings(user_id, role_name):
    if role_name == "Franchisee":
        franchisee = Franchisee.query.filter_by(user_id=user_id).first()
        if not franchisee:
            return {"msg": "Franchisee not found"}, 404

        total_earnings = db.session.query(func.sum(Commission.amount))\
            .filter(Commission.franchisee_id == franchisee.franchisee_id).scalar() or 0

        return {
            "franchisee_id": franchisee.franchisee_id,
            "franchisee_name": franchisee.user.full_name,
            "total_earnings": float(total_earnings)
        }, 200

    elif role_name in ["Franchisor", "Admin"]:
        earnings = db.session.query(
            Franchisee.franchisee_id,
            User.full_name,
            func.sum(Commission.amount).label("total_earnings")
        ).join(User, Franchisee.user_id == User.user_id)\
         .join(Commission, Franchisee.franchisee_id == Commission.franchisee_id)\
         .group_by(Franchisee.franchisee_id, User.full_name).all()

        return {
            "franchise_earnings": [
                {
                    "franchisee_id": e.franchisee_id,
                    "franchisee_name": e.full_name,
                    "total_earnings": float(e.total_earnings or 0)
                } for e in earnings
            ]
        }, 200

    return {"msg": "Unauthorized"}, 403

def request_withdrawal(user_id, data):
    amount = data.get("amount")
    payment_method = data.get("payment_method")

    if not amount or not payment_method or not isinstance(amount, (int, float)) or amount <= 0:
        return {"msg": "Invalid amount or payment method"}, 400

    # Get franchisee
    franchisee = Franchisee.query.filter_by(user_id=user_id).first()
    if not franchisee:
        return {"msg": "Franchisee not found"}, 404

    # Calculate total earnings
    total_earnings = db.session.query(func.sum(Commission.amount))\
        .filter(Commission.franchisee_id == franchisee.franchisee_id).scalar() or 0

    # Total withdrawn (optional if you track it separately)
    total_withdrawn = db.session.query(func.sum(Withdrawal.amount))\
        .filter(Withdrawal.franchisee_id == franchisee.franchisee_id,
                Withdrawal.status.has(status_name="approved")).scalar() or 0

    available_balance = float(total_earnings) - float(total_withdrawn)

    if amount > available_balance:
        return {"msg": f"Insufficient balance. Available: {available_balance}"}, 400

    # Get PENDING status
    pending_status = Status.query.filter_by(status_name="pending").first()
    if not pending_status:
        return {"msg": "Pending status not found"}, 500

    # Create withdrawal request
    withdrawal = Withdrawal(
        franchisee_id=franchisee.franchisee_id,
        amount=amount,
        payment_method=payment_method,
        status_id=pending_status.status_id,
        requested_time=datetime.now(UTC)
    )
    db.session.add(withdrawal)
    db.session.commit()

    return {
        "msg": "Withdrawal request submitted",
        "withdrawal_id": withdrawal.withdrawal_id,
        "status": "pending"
    }, 201


def get_withdrawl_request():
    user_id = get_jwt_identity()
    claims = get_jwt()
    role = claims.get("role_name")

    if role == "Franchisee":
        user = User.query.get(user_id)
        if not user or not user.franchisee:
            return {"msg": "Franchisee not found"}, 404

        withdrawals = Withdrawal.query.filter_by(franchisee_id=user.franchisee.franchisee_id).all()
    elif role in ["Admin", "Franchisor"]:
        withdrawals = Withdrawal.query.all()
    else:
        return {"msg": "Unauthorized"}, 403

    result = []
    for w in withdrawals:
        result.append({
            "withdrawal_id": w.withdrawal_id,
            "franchisee_id": w.franchisee_id,
            "franchisee_name": w.franchisee.user.full_name,
            "amount": float(w.amount),
            "payment_method": w.payment_method,
            "status": w.status.status_name,
            "created_time": w.created_time.isoformat(),
            "completed_at": w.completed_at.isoformat() if w.completed_at else None
        })

    return result, 200

