from fms import db
from datetime import datetime,UTC
from fms.models.Role import Role

utc_now = datetime.now(UTC)

class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(1000), nullable=False)
    phone_no = db.Column(db.Numeric(10), nullable=False, unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.role_id'))
    is_active = db.Column(db.Boolean, default=True)
    created_time = db.Column(db.TIMESTAMP, default=utc_now)
    updated_time = db.Column(db.TIMESTAMP, default=utc_now, onupdate=utc_now)

    role = db.relationship('Role', backref="user")