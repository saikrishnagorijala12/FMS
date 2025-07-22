from datetime import datetime
from flask_jwt_extended import get_jwt, get_jwt_identity
from fms.models import User, Order, Payment, Franchisee, StockRequest, Withdrawal, Commission, Inventory
from fms import db
from sqlalchemy import func, extract


def get_dashboard():
    claims = get_jwt()
    user_id = get_jwt_identity()
    role = claims.get("role_name")

    data = {}

    if role == "Admin":
        data['total_users'] = User.query.count()
        data['total_sales'] = float(db.session.query(func.sum(Payment.amount)).scalar() or 0)
        data['total_orders'] = Order.query.count()
        data['total_stock_requests'] = StockRequest.query.count()
        data['pending_withdrawals'] = Withdrawal.query.filter_by(status_id=1).count()
        data['total_commissions'] = float(db.session.query(func.sum(Commission.amount)).scalar() or 0)

    elif role == "Franchisor":
        data['total_franchisees'] = Franchisee.query.count()
        data['total_sales'] = float(db.session.query(func.sum(Payment.amount)).scalar() or 0)
        data['total_orders'] = Order.query.count()
        data['pending_stock_requests'] = StockRequest.query.filter_by(status_id=1).count()
        data['pending_withdrawals'] = Withdrawal.query.filter_by(status_id=1).count()
        data['total_commissions'] = float(db.session.query(func.sum(Commission.amount)).scalar() or 0)

    elif role == "Franchisee":
        franchisee = Franchisee.query.filter_by(user_id=user_id).first()
        if not franchisee:
            return {"msg": "Franchisee not found"}, 404

        fid = franchisee.franchisee_id

        data['my_sales'] = float(db.session.query(func.sum(Payment.amount))
                                 .join(Order).filter(Order.franchisee_id == fid).scalar() or 0)
        data['my_orders'] = Order.query.filter_by(franchisee_id=fid).count()
        data['my_stock_requests'] = StockRequest.query.filter_by(franchisee_id=fid).count()
        data['my_withdrawals'] = Withdrawal.query.filter_by(franchisee_id=fid).count()
        data['my_earnings'] = float(db.session.query(func.sum(Commission.amount))
                                    .filter_by(franchisee_id=fid).scalar() or 0)

    else:
        return {"msg": "Unauthorized"}, 403

    return data, 200

def get_sales(data):
    claims = get_jwt()
    user_id = get_jwt_identity()
    role = claims.get('role_name')

    if role not in ['Admin', 'Franchisor', 'Franchisee']:
        return {'msg': 'Unauthorized'}, 403

    interval = data.args.get('interval', 'month')
    from_date = data.args.get('from')
    to_date = data.args.get('to')

    query = db.session.query(
        Payment.amount,
        Payment.created_time,
        Order.franchisee_id
    ).join(Order, Payment.order_id == Order.order_id)

    if from_date:
        from_date = datetime.strptime(from_date, "%Y-%m-%d")
        query = query.filter(Payment.created_time >= from_date)
    if to_date:
        to_date = datetime.strptime(to_date, "%Y-%m-%d")
        query = query.filter(Payment.created_time <= to_date)

    if role == 'Franchisee':
        franchisee = Franchisee.query.filter_by(user_id=user_id).first()
        if not franchisee:
            return {"msg": "Franchisee not found"}, 404
        query = query.filter(Order.franchisee_id == franchisee.franchisee_id)

    if interval == 'day':
        group_by = [func.date(Payment.created_time)]
        label = func.date(Payment.created_time).label("period")
    elif interval == 'year':
        group_by = [extract('year', Payment.created_time)]
        label = func.concat(extract('year', Payment.created_time)).label("period")
    else:  # default: month
        group_by = [extract('year', Payment.created_time), extract('month', Payment.created_time)]
        label = func.concat(
            extract('year', Payment.created_time), '-',
            func.lpad(extract('month', Payment.created_time).cast(db.Text), 2, '0')
        ).label("period")

    results = db.session.query(
        label,
        func.sum(Payment.amount).label("total_sales")
    ).join(Order, Payment.order_id == Order.order_id).group_by(*group_by).order_by(label).all()

    sales_data = [{"period": r.period, "total_sales": float(r.total_sales)} for r in results]

    return {
        "interval": interval,
        "data": sales_data
    }, 200


def get_inventory_data():
    items = Inventory.query.all()
    return [{
        "product_id": item.product_id,
        "product_name": item.product.name,
        "quantity": item.quantity
    } for item in items], 200


def get_customer_data():
    return [{
        "user_id": user.user_id,
        "name": user.full_name,
        "email": user.email
    } for user in User.query.filter_by(role_id=2).all()], 200


def get_franchise_performance():
    results = db.session.query(
        Franchisee.franchisee_id,
        Franchisee.store_name,
        func.sum(Order.total_amount)
    ).join(Order).group_by(Franchisee.franchisee_id).all()

    return [{
        "franchisee_id": fid,
        "store_name": name,
        "total_sales": float(sales)
    } for fid, name, sales in results], 200