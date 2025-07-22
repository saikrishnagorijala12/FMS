from fms import db
from datetime import datetime,UTC
from fms.models.User import User

utc_now = datetime.now(UTC)


class Franchisor(db.Model):
    __tablename__ = 'franchisor'
    franchisor_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'), unique=True, nullable=False)
    company_name = db.Column(db.String(100))
    headquarters_address = db.Column(db.Text)

    user = db.relationship("User", backref="franchisor")
