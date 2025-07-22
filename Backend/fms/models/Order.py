from fms import db
from datetime import datetime,UTC
from fms.models.Franchisee import Franchisee
from fms.models.Customer import Customer
from fms.models.Status import Status

utc_now = datetime.now(UTC)


class Order(db.Model):
    __tablename__ = 'order'
    
    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_display_id = db.Column(db.String(30), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id', ondelete='CASCADE'))
    franchisee_id = db.Column(db.Integer, db.ForeignKey('franchisee.franchisee_id', ondelete='CASCADE'))
    total_amount = db.Column(db.Numeric(10,2), nullable=False)
    delivery_address = db.Column(db.Text)
    status_id = db.Column(db.Integer, db.ForeignKey('status.status_id', ondelete='CASCADE'), nullable=False)
    created_time = db.Column(db.TIMESTAMP, default=utc_now)


    franchisee = db.relationship("Franchisee", backref="order")
    customer = db.relationship("Customer", backref="order")
    status = db.relationship("Status", backref="order")