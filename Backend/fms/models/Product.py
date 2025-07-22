from fms import db
from datetime import datetime,UTC
from fms.models.Franchisor import Franchisor

utc_now = datetime.now(UTC)


class Product(db.Model):
    __tablename__ = 'product'

    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    category = db.Column(db.String(50))  # NEW
    rating = db.Column(db.Float, default=0.0)  # NEW
    reviews = db.Column(db.Integer, default=0)  # NEW
    franchisor_id = db.Column(db.Integer, db.ForeignKey('franchisor.franchisor_id', ondelete='CASCADE'))
    created_time = db.Column(db.TIMESTAMP, default=utc_now)

    franchisor = db.relationship("Franchisor", backref="product")