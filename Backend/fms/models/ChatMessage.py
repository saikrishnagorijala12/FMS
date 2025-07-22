from fms import db
from datetime import datetime,UTC
from fms.models.User import User




utc_now = datetime.now(UTC)


class ChatMessage(db.Model):
    __tablename__ = 'chat_message'
    
    message_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'))
    message = db.Column(db.Text)
    created_time = db.Column(db.TIMESTAMP, default=utc_now)

    sender = db.relationship('User', foreign_keys=[sender_id])
    receiver = db.relationship('User', foreign_keys=[receiver_id])
