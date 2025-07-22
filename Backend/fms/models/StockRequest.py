from fms import db
from datetime import datetime,UTC
from fms.models.Franchisee import Franchisee
from fms.models.Status import Status
from fms.models.Product import Product

utc_now = datetime.now(UTC)


class StockRequest(db.Model):
    __tablename__ = 'stock_request'
    
    request_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    franchisee_id = db.Column(db.Integer, db.ForeignKey('franchisee.franchisee_id', ondelete='CASCADE'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id', ondelete='CASCADE'))
    quantity = db.Column(db.Integer,nullable=False)
    urgency = db.Column(db.String(150), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('status.status_id', ondelete='CASCADE'), nullable=False)
    created_time = db.Column(db.TIMESTAMP, default=utc_now)

    franchisee = db.relationship("Franchisee", backref="stock_request")
    product = db.relationship("Product", backref="stock_request")
    status = db.relationship("Status", backref="product")