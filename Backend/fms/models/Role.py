from fms import db

class Role(db.Model):
    __tablename__ = 'role'
    role_id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    role_name = db.Column(db.String(12), nullable=False)