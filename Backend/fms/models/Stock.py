from fms import db
from datetime import datetime, UTC
from fms.models.Franchisor import Franchisor
# from fms.models.Product import Product

utc_now = datetime.now(UTC)
#
# class Stock(db.Model):
#     __tablename__ = 'stock'
#
#     stock_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     product_id = db.Column(db.Integer, db.ForeignKey('product.product_id', ondelete='CASCADE'), nullable=False)
#     franchisor_id = db.Column(db.Integer, db.ForeignKey('franchisor.franchisor_id', ondelete='CASCADE'), nullable=False)
#     quantity = db.Column(db.Integer, nullable=False, default=0)
#
#     product = db.relationship("Product", backref="stock")
#     franchisor = db.relationship("Franchisor", backref="stock")
#
#     __table_args__ = (
#         db.UniqueConstraint('product_id', 'franchisor_id', name='uix_product_franchisee'),
#     )

class Stock(db.Model):
    __tablename__ = 'stock'

    stock_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(
        db.Integer,
        db.ForeignKey('product.product_id', ondelete='CASCADE'),
        nullable=False
    )
    franchisor_id = db.Column(
        db.Integer,
        db.ForeignKey('franchisor.franchisor_id', ondelete='CASCADE'),
        nullable=False
    )
    quantity = db.Column(db.Integer, nullable=False, default=0)

    franchisor = db.relationship(
        "Franchisor",
        backref=db.backref("stocks", cascade="all, delete-orphan", passive_deletes=True)
    )

    __table_args__ = (
        db.UniqueConstraint('product_id', 'franchisor_id', name='uix_product_franchisee'),
    )
