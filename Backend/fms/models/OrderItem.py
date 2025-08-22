from fms import db
from datetime import datetime,UTC
from fms.models.Order import Order
from fms.models.Product import Product

utc_now = datetime.now(UTC)


class OrderItem(db.Model):
    __tablename__ = 'order_item'
    
    order_item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.order_id', ondelete='CASCADE'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id', ondelete='CASCADE'))
    quantity = db.Column(db.Integer,nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    created_time = db.Column(db.TIMESTAMP, default=utc_now)

    order = db.relationship("Order", backref=db.backref("order_items", cascade="all, delete-orphan", lazy=True))
    product = db.relationship("Product", backref="order_item")