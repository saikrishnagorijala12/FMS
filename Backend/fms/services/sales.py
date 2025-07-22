from sqlalchemy import func
from fms import db
from fms.models import Payment, Commission, Withdrawal, Order, Status, Franchisee


def get_sales_data(user_id):
    # Look up the franchisee for this user
    franchisee = Franchisee.query.filter_by(user_id=user_id).first()
    if not franchisee:
        return {"error": "No franchisee found for this user"}, 404

    franchisee_id = franchisee.franchisee_id

    # Now run your existing aggregation function
    sales_data = get_sales_for_franchisee(franchisee_id)
    return sales_data, 200


def get_sales_for_franchisee(franchisee_id: int):
    total_sales = (
        db.session.query(func.coalesce(func.sum(Payment.amount), 0))
        .join(Order, Payment.order_id == Order.order_id)
        .filter(Order.franchisee_id == franchisee_id)
        .scalar()
    )

    total_revenue = (
        db.session.query(func.coalesce(func.sum(Commission.amount), 0))
        .filter(Commission.franchisee_id == franchisee_id)
        .scalar()
    )

    commission_paid = (
        db.session.query(func.coalesce(func.sum(Commission.amount), 0))
        .filter(
            Commission.franchisee_id == franchisee_id,
            Commission.status_id == 9  # 'paid'
        )
        .scalar()
    )

    withdrawn_earnings = (
        db.session.query(func.coalesce(func.sum(Withdrawal.amount), 0))
        .filter(Withdrawal.franchisee_id == franchisee_id)
        .scalar()
    )

    return {
        "totalSales": float(total_sales),
        "totalRevenue": float(total_revenue),
        "commissionPaid": float(commission_paid),
        "withdrawnEarnings": float(withdrawn_earnings)
    }


def getUnpaidCommisions(user_id):
    franchisee = Franchisee.query.filter_by(user_id=user_id).first()
    if not franchisee:
        return {"error": "Franchisee not found for this user"}, 404

    # Step 2: Query unpaid commissions
    unpaid_commissions = (
        Commission.query
        .filter(
            Commission.franchisee_id == franchisee.franchisee_id,
            Commission.status_id != 9  # not paid
        )
        .all()
    )

    # Step 3: Build list and calculate total
    total_unpaid_amount = 0
    data = []

    for commission in unpaid_commissions:
        amt = float(commission.amount)
        total_unpaid_amount += amt
        data.append({
            "commission_id": commission.commission_id,
            "order_id": commission.order_id,
            "amount": amt,
            "rate": float(commission.rate),
            "status_id": commission.status_id,
            "status_name": commission.status.status_name if commission.status else None,
            "created_time": commission.created_time.isoformat() if commission.created_time else None,
            "paid_at": commission.paid_at.isoformat() if commission.paid_at else None,
        })

    # Step 4: Return with total
    return {
        "total_unpaid_amount": total_unpaid_amount,
        # "commissions": data
    }, 200