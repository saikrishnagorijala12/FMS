from fms import db
from datetime import datetime,UTC
from fms.models.Order import Order
from fms.models.Status import Status


utc_now = datetime.now(UTC)


class Payment(db.Model):
    __tablename__ = 'payment'
    
    payment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.order_id', ondelete='CASCADE'))
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_method = db.Column(db.String(50))
    status_id = db.Column(db.Integer, db.ForeignKey('status.status_id', ondelete='CASCADE'), nullable=False)
    created_time = db.Column(db.TIMESTAMP, default=utc_now)

    order = db.relationship("Order", backref="payment")
    status = db.relationship("Status", backref="payment")