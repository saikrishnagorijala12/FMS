from fms.models import Customer
from fms.models.User import User
from fms.models.Order import Order
from fms.models.Status import Status
from fms import db

def get_customers():
    customers = User.query.filter_by(role_id=2).all()
    return [
        {
            "user_id": c.user_id,
            "full_name": c.full_name,
            "email": c.email,
            "phone": c.phone,
            "status": c.status.status_name if c.status else None
        } for c in customers
    ], 200

def get_customer_details(customer_id):
    customer = User.query.filter_by(user_id=customer_id, role_id=2).first()
    if not customer:
        return {"msg": "Customer not found"}, 404

    return {
        "user_id": customer.user_id,
        "full_name": customer.full_name,
        "email": customer.email,
        "phone": customer.phone,
        "status": customer.status.status_name if customer.status else None
    }, 200

def get_customer_orders(customer_id):
    orders = Order.query.filter_by(user_id=customer_id).all()
    return [
        {
            "order_id": o.order_id,
            "total_amount": float(o.total_amount),
            "status": o.status.status_name,
            "created_time": o.created_time
        } for o in orders
    ], 200

def fetch_customer_address(customer_id):
    customers = Customer.query.filter_by(user_id=customer_id).all()
    return [
        {
            "customer_id": c.customer_id,
            "user_id": c.user_id,
            "address": c.address
        } for c in customers
    ], 200


def update_customer_status(customer_id, data):
    new_status = data.get("status_name")
    if not new_status:
        return {"msg": "Missing status_name"}, 400

    customer = User.query.filter_by(user_id=customer_id, role_id=2).first()
    if not customer:
        return {"msg": "Customer not found"}, 404

    status = Status.query.filter_by(status_name=new_status.upper()).first()
    if not status:
        return {"msg": f"Status '{new_status}' not valid"}, 400

    customer.status_id = status.status_id
    db.session.commit()

    return {"msg": "Customer status updated successfully"}, 200


def post_customer_address(user_id: int, data: dict):
    try:
        # ✅ Find customer by user_id (not primary key)
        customer = Customer.query.filter_by(user_id=user_id).first()
        if not customer:
            return {"message": f"No customer found for user_id={user_id}"}, 404

        # ✅ Extract address from request body
        address = data.get("address")
        if not address:
            return {"message": "Address is required"}, 400

        # ✅ Update address and commit
        customer.address = address
        db.session.commit()

        return {
            "message": "Address updated successfully",
            "customer_id": customer.customer_id,
            "user_id": customer.user_id,
            "address": customer.address
        }, 200

    except Exception as e:
        db.session.rollback()
        return {"message": "Internal server error", "error": str(e)}, 500