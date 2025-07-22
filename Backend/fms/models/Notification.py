from fms import db
from datetime import datetime, UTC
from fms.models.User import User

utc_now = datetime.now(UTC)

class Notification(db.Model):
    __tablename__ = 'notification'

    notification_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_time = db.Column(db.TIMESTAMP, default=utc_now)

    user = db.relationship("User", backref="notifications")
