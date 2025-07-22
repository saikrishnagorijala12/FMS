from fms import db
from fms.models.Notification import Notification

def get_user_notifications(user_id):
    notifications = Notification.query.filter_by(user_id=user_id).order_by(Notification.created_time.desc()).all()
    return [{
        "notification_id": n.notification_id,
        "message": n.message,
        "is_read": n.is_read,
        "created_time": n.created_time
    } for n in notifications], 200

def mark_as_read(user_id, notification_id):
    notif = Notification.query.filter_by(notification_id=notification_id, user_id=user_id).first()
    if not notif:
        return {"msg": "Notification not found"}, 404

    notif.is_read = True
    db.session.commit()
    return {"msg": "Notification marked as read"}, 200

def mark_all_as_read(user_id):
    Notification.query.filter_by(user_id=user_id, is_read=False).update({ "is_read": True })
    db.session.commit()
    return {"msg": "All notifications marked as read"}, 200

def delete_notification(user_id, notification_id):
    notif = Notification.query.filter_by(notification_id=notification_id, user_id=user_id).first()
    if not notif:
        return {"msg": "Notification not found"}, 404

    db.session.delete(notif)
    db.session.commit()
    return {"msg": "Notification deleted"}, 200
