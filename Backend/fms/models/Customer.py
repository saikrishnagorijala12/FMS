from fms import db
from datetime import datetime,UTC
from fms.models.User import User

utc_now = datetime.now(UTC)


class Customer(db.Model):
    __tablename__ = 'customer'
    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'), unique=True, nullable=False)
    address = db.Column(db.Text)

    user = db.relationship("User", backref="customer")
