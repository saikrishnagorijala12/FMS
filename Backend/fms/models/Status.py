from fms import db

class Status(db.Model):
    __tablename__ = 'status'
    status_id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    status_name = db.Column(db.String(10), nullable=False)