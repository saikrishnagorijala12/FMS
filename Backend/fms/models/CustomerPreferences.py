from fms import db
from datetime import datetime,UTC
from fms.models.Customer import Customer

utc_now = datetime.now(UTC)

class CustomerPreferences(db.Model):
    __tablename__ = 'customer_preferences'

    preference_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'), nullable=False)
    preferences = db.Column(db.Text)
    email_notifications = db.Column(db.Boolean, default=True, nullable=False)
    sms_notifications = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=utc_now)
    updated_at = db.Column(db.DateTime, default=utc_now, onupdate=utc_now)

    # optional: relationship back to customer
    customer = db.relationship("Customer", backref="customer_preferences")
