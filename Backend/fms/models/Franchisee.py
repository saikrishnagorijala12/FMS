from fms import db
from datetime import datetime,UTC
from fms.models.Franchisor import Franchisor
from fms.models.User import User
from fms.models.Status import Status

utc_now = datetime.now(UTC)


class Franchisee(db.Model):
    __tablename__ = 'franchisee'
    franchisee_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'), unique=True, nullable=False)
    franchisor_id = db.Column(db.Integer, db.ForeignKey('franchisor.franchisor_id', ondelete='SET NULL'))
    region = db.Column(db.String(100))
    status_id = db.Column(db.Integer, db.ForeignKey('status.status_id', ondelete='CASCADE'), nullable=False)
    

    user = db.relationship("User", backref="franchisee")
    franchisor = db.relationship("Franchisor", backref="franchisee")
    status = db.relationship("Status", backref="franchisee")
