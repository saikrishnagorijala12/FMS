from fms import db
from fms.models import Customer
from fms.models.CustomerPreferences import CustomerPreferences


def fetch_prefernce(customer_id):
    customer = Customer.query.filter_by(user_id=customer_id).first()
    if not customer:
        return {"message": "Customer not found for this user"}, 404
    prefs = CustomerPreferences.query.filter_by(customer_id=customer.customer_id).first()
    if not prefs:
        return {"message": "Preferences not found for this customer"}, 404

    return {
        'customer_id': prefs.customer_id,
        'preferences': prefs.preferences,
        'emailNotifications': prefs.email_notifications,
        'smsNotifications': prefs.sms_notifications
    }, 200


def update_preference(customer_id, data):
    customer = Customer.query.filter_by(user_id=customer_id).first()
    if not customer:
        return {"message": "Customer not found for this user"}, 404
    prefs = CustomerPreferences.query.filter_by(customer_id=customer.customer_id).first()
    if not prefs:
        return {"message": "Preferences not found for this customer"}, 404

    prefs.preferences = data.get('preferences', prefs.preferences)
    prefs.email_notifications = data.get('emailNotifications', prefs.email_notifications)
    prefs.sms_notifications = data.get('smsNotifications', prefs.sms_notifications)

    db.session.add(prefs)
    db.session.commit()

    return {
        'message': 'Preferences saved successfully',
        'customer_id': prefs.customer_id,
        'preferences': prefs.preferences,
        'emailNotifications': prefs.email_notifications,
        'smsNotifications': prefs.sms_notifications
    }, 200