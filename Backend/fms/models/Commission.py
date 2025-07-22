from fms import db
from datetime import datetime,UTC
from fms.models.Franchisee import Franchisee
from fms.models.Franchisor import Franchisor
from fms.models.Order import Order
from fms.models.Status import Status



utc_now = datetime.now(UTC)


class Commission(db.Model):
    __tablename__ = 'commission'
    
    commission_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    franchisee_id = db.Column(db.Integer, db.ForeignKey('franchisee.franchisee_id', ondelete='CASCADE'))
    franchisor_id = db.Column(db.Integer, db.ForeignKey('franchisor.franchisor_id', ondelete='CASCADE'))
    order_id = db.Column(db.Integer, db.ForeignKey('order.order_id', ondelete='CASCADE'))
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    rate = db.Column(db.Numeric(5, 2), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('status.status_id', ondelete='CASCADE'), nullable=False)
    paid_at = db.Column(db.TIMESTAMP)
    created_time = db.Column(db.TIMESTAMP, default=utc_now)

    franchisee = db.relationship("Franchisee", backref="commission")
    franchisor = db.relationship("Franchisor", backref="commission")
    order = db.relationship("Order", backref="commission")
    status = db.relationship("Status", backref="commission")