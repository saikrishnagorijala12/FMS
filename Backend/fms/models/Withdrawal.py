from fms import db
from datetime import datetime,UTC
from fms.models.Franchisee import Franchisee
from fms.models.Status import Status



utc_now = datetime.now(UTC)


class Withdrawal(db.Model):
    __tablename__ = 'withdrawal'

    withdrawal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    franchisee_id = db.Column(db.Integer, db.ForeignKey('franchisee.franchisee_id', ondelete='CASCADE'))
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('status.status_id', ondelete='CASCADE'), nullable=False)
    completed_at = db.Column(db.TIMESTAMP)
    created_time = db.Column(db.TIMESTAMP, default=lambda: datetime.now(UTC))

    franchisee = db.relationship("Franchisee", backref="withdrawals")
    status = db.relationship("Status", backref="withdrawals")