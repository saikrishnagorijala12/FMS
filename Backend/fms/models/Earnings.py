from fms import db
from datetime import datetime,UTC
from fms.models.Franchisee import Franchisee



utc_now = datetime.now(UTC)


class Earnings(db.Model):
    __tablename__ = 'earnings'
    
    earnings_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    franchisee_id = db.Column(db.Integer, db.ForeignKey('franchisee.franchisee_id', ondelete='CASCADE'))
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    period = db.Column(db.String(20))
    created_time = db.Column(db.TIMESTAMP, default=utc_now)

    franchisee = db.relationship("Franchisee", backref="earnings")