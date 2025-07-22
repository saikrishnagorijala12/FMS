from fms import db
from datetime import datetime, UTC
from fms.models.Franchisee import Franchisee
from fms.models.Product import Product

utc_now = datetime.now(UTC)

class Inventory(db.Model):
    __tablename__ = 'inventory'

    inventory_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id', ondelete='CASCADE'), nullable=False)
    franchisee_id = db.Column(db.Integer, db.ForeignKey('franchisee.franchisee_id', ondelete='CASCADE'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)

    product = db.relationship("Product", backref="inventories")
    franchisee = db.relationship("Franchisee", backref="inventories")

    __table_args__ = (
        db.UniqueConstraint('product_id', 'franchisee_id', name='uix_product_franchisee'),
    )
