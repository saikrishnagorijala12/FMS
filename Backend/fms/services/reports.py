from fms.models.Earnings import Earnings
from fms.models.Order import Order
from fms.models.OrderItem import OrderItem
from fms.models.Product import Product
from fms.models.Commission import Commission
from fms.models.Payment import Payment
from fms.models.Franchisee import Franchisee
from fms.models.Inventory import Inventory
from fms.models.Withdrawal import Withdrawal
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


def get_franchisor_report():
    top_franchise = db.session.query(
        Franchisee.region, db.func.count(Order.order_id).label("orders")
    ).join(Order).group_by(Franchisee.region).order_by(db.desc("orders")).first()

    best_product = db.session.query(
        Product.name, db.func.sum(OrderItem.quantity).label("sold")
    ).join(OrderItem).group_by(Product.name).order_by(db.desc("sold")).first()

    avg_order_value = db.session.query(db.func.avg(Order.total_amount)).scalar() or 0

    monthly_growth = 12.5
    commission_collected = db.session.query(db.func.sum(Commission.amount)).scalar() or 0
    outstanding_payments = db.session.query(
        db.func.sum(Payment.amount)
    ).filter_by(status_id=2).scalar() or 0

    active_franchises = Franchisee.query.count()
    underperforming = 2
    expansion_opportunities = 5

    return {
        "performanceSummary": {
            "topFranchise": top_franchise.region if top_franchise else "N/A",
            "bestProduct": best_product.name if best_product else "N/A",
            "averageOrderValue": round(float(avg_order_value),3),
        },
        "financialAnalytics": {
            "monthlyGrowth": monthly_growth,
            "commissionCollected": float(commission_collected),
            "outstandingPayments": float(outstanding_payments),
        },
        "franchiseHealth": {
            "activeFranchises": active_franchises,
            "underperforming": underperforming,
            "expansionOpportunities": expansion_opportunities,
        }
    }, 200


def get_franchise_report(user_id):
    franchisee = Franchisee.query.filter_by(user_id=user_id).first()
    if not franchisee:
        return {"error": "No franchisee found for this user"}, 404

    franchisee_id = franchisee.franchisee_id
    total_orders = Order.query.filter_by(franchisee_id=franchisee_id).count()
    total_sales = db.session.query(db.func.sum(Order.total_amount)) \
                      .filter(Order.franchisee_id == franchisee_id).scalar() or 0

    best_product = db.session.query(
        Product.name, db.func.sum(OrderItem.quantity).label("sold")
    ).join(OrderItem).join(Order) \
        .filter(Order.franchisee_id == franchisee_id) \
        .group_by(Product.name).order_by(db.desc("sold")).first()

    avg_order_value = db.session.query(db.func.avg(Order.total_amount)) \
                          .filter(Order.franchisee_id == franchisee_id).scalar() or 0


    total_commission = db.session.query(db.func.sum(Commission.amount)) \
                           .filter(Commission.franchisee_id == franchisee_id).scalar() or 0


    total_earnings = db.session.query(db.func.sum(Earnings.amount)) \
                         .filter(Earnings.franchisee_id == franchisee_id).scalar() or 0


    total_withdrawn = db.session.query(db.func.sum(Withdrawal.amount)) \
                          .filter(Withdrawal.franchisee_id == franchisee_id).scalar() or 0

    balance = total_earnings - total_withdrawn

    return {
        "userId": user_id,
        "franchiseId": franchisee_id,
        "orders": {
            "totalOrders": total_orders,
            "totalSales": float(total_sales),
            "averageOrderValue": round(float(avg_order_value),2),
            "bestProduct": best_product.name if best_product else "N/A"
        },
        "commissions": {
            "totalCommission": float(total_commission)
        },
        "earnings": {
            "totalEarnings": float(total_earnings),
            "withdrawn": float(total_withdrawn),
            "balance": float(balance)
        }
    }, 200