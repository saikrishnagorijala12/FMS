from fms import db
from datetime import datetime, UTC
from fms.models.Franchisee import Franchisee
from fms.models.Franchisor import Franchisor
from fms.models.Status import Status

utc_now = datetime.now(UTC)


class FranchiseApplication(db.Model):
    __tablename__ = 'franchise_application'

    application_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    application_display_id = db.Column(db.String(30), unique=True, nullable=False)  # e.g., APP-001
    franchisee_id = db.Column(db.Integer, db.ForeignKey('franchisee.franchisee_id', ondelete='CASCADE'))
    franchisor_id = db.Column(db.Integer, db.ForeignKey('franchisor.franchisor_id', ondelete='CASCADE'))
    region = db.Column(db.String(100))
    investment = db.Column(db.Numeric(12, 2), nullable=True)  # investment amount
    experience = db.Column(db.String(255), nullable=True)  # experience description
    status_id = db.Column(db.Integer, db.ForeignKey('status.status_id', ondelete='CASCADE'), nullable=False)
    created_time = db.Column(db.TIMESTAMP, default=utc_now)

    franchisee = db.relationship("Franchisee", backref="franchise_application")
    franchisor = db.relationship("Franchisor", backref="franchise_application")
    status = db.relationship("Status", backref="franchise_application")
