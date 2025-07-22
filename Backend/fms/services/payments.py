from fms.models.Payment import Payment
from fms.models.Order import Order
from fms.models.Status import Status
from fms import db
from datetime import datetime, UTC
from sqlalchemy.orm import joinedload

def process_payment(data, user_id, role_name):
    order_id = data.get("order_id")
    amount = data.get("amount")
    method = data.get("payment_method")

    if not order_id or not amount or not method:
        return {"message": "Missing order_id, amount or payment_method"}, 400

    order = Order.query.get(order_id)
    if not order:
        return {"message": "Order not found"}, 404

    # Role-based ownership check
    if role_name.lower() == "customer" and order.user_id != user_id:
        return {"message": "Unauthorized to pay for this order"}, 403

    # Get 'paid' status
    paid_status = Status.query.filter_by(status_name='paid').first()
    if not paid_status:
        return {"message": "Payment status 'paid' not found in status table"}, 500

    # Create payment
    payment = Payment(
        order_id=order_id,
        amount=amount,
        payment_method=method,
        status_id=paid_status.status_id,
        created_time=datetime.now(UTC)
    )
    db.session.add(payment)

    # Optionally: update order's status to 'paid' too
    order.status_id = paid_status.status_id

    db.session.commit()

    return {
        "message": "Payment processed successfully",
        "payment_id": payment.payment_id,
        "order_id": order_id,
        "amount": str(payment.amount),
        "payment_method": method,
        "payment_status": paid_status.status_name
    }, 201


def get_payments(role_name, user_id):
    payments_query = Payment.query.options(
        joinedload(Payment.order),
        joinedload(Payment.status)
    )

    if role_name.lower() == "customer":
        # Filter payments by user's orders
        payments_query = payments_query.join(Order).filter(Order.user_id == user_id)

    payments = payments_query.order_by(Payment.created_time.desc()).all()

    result = []
    for payment in payments:
        result.append({
            "payment_id": payment.payment_id,
            "order_id": payment.order_id,
            "amount": str(payment.amount),
            "payment_method": payment.payment_method,
            "status": payment.status.status_name if payment.status else None,
            "created_time": payment.created_time.isoformat()
        })

    return result, 200

def get_payment_by_id(payment_id, user_id, role_name):
    query = Payment.query.join(Order).options(
        db.joinedload(Payment.order),
        db.joinedload(Payment.status)
    ).filter(Payment.payment_id == payment_id)

    if role_name.lower() == "customer":
        query = query.filter(Order.user_id == user_id)

    payment = query.first()

    if not payment:
        return {"message": "Payment not found or unauthorized"}, 404

    return {
        "payment_id": payment.payment_id,
        "order_id": payment.order_id,
        "amount": str(payment.amount),
        "payment_method": payment.payment_method,
        "status": payment.status.status_name if payment.status else None,
        "created_time": payment.created_time.isoformat()
    }, 200

def process_refund(payment_id, role_name):
    if role_name not in ["Admin", "Franchisor"]:
        return {"message": "Unauthorized"}, 403

    payment = Payment.query.get(payment_id)
    if not payment:
        return {"message": "Payment not found"}, 404

    if payment.status.status_name.lower() == "refunded":
        return {"message": "Payment already refunded"}, 400

    # You can optionally check for time-based eligibility (e.g., within 7 days)

    # Update the payment status to 'refunded'
    refund_status = Status.query.filter_by(status_name="refunded").first()
    if not refund_status:
        return {"message": "'refunded' status not found in system"}, 500

    payment.status_id = refund_status.status_id
    payment.created_time = datetime.now(UTC)
    db.session.commit()

    return {
        "message": "Refund processed successfully",
        "payment_id": payment.payment_id,
        "status": refund_status.status_name
    }, 200