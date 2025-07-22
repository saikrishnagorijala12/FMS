from fms.models.Order import Order
from fms.models.Inventory import Inventory
from fms.models.Payment import Payment
from sqlalchemy import func
from fms import db

def generate_sales_report():
    sales = db.session.query(
        func.date(Order.created_time),
        func.count(Order.order_id),
        func.sum(Order.total_amount)
    ).group_by(func.date(Order.created_time)).all()

    return [{
        "date": str(date),
        "orders": count,
        "total_sales": float(amount)
    } for date, count, amount in sales], 200

def generate_inventory_report():
    items = Inventory.query.all()
    return [{
        "inventory_id": item.inventory_id,
        "product_name": item.product.name,
        "quantity": item.quantity
    } for item in items], 200

def generate_financial_report():
    payments = db.session.query(
        func.date(Payment.created_time),
        func.sum(Payment.amount)
    ).group_by(func.date(Payment.created_time)).all()

    return [{
        "date": str(date),
        "total_payments": float(amount)
    } for date, amount in payments], 200
