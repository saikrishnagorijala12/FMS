from fms import db
from datetime import datetime,UTC
from fms.models.Franchisee import Franchisee

utc_now = datetime.now(UTC)


class FranchiseLocation(db.Model):
    __tablename__ = 'franchise_location'
    
    location_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    franchisee_id = db.Column(db.Integer, db.ForeignKey('franchisee.franchisee_id', ondelete='CASCADE'))
    name = db.Column(db.String(150), nullable=False)  # location name
    phone = db.Column(db.String(20), nullable=True)  # phone number
    hours = db.Column(db.String(255), nullable=True)  # opening hours
    services = db.Column(db.JSON, nullable=True)
    address = db.Column(db.Text)
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    zipcode = db.Column(db.String(20))
    created_time = db.Column(db.TIMESTAMP, default=utc_now)

    franchisee = db.relationship("Franchisee", backref="franchise_location")