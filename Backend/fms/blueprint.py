from fms.routes.auth import auth_bp
from fms.routes.users import user_bp
from fms.routes.franchises import franchises_bp
from fms.routes.products import products_bp
from fms.routes.orders import orders_bp
from fms.routes.payments import payments_bp
from fms.routes.finances import finances_bp
from fms.routes.analytics import analytics_bp
from fms.routes.reports import reports_bp
from fms.routes.customer import customer_bp
from fms.routes.notification import notification_bp
from fms.routes.browse import browse_bp
from fms.routes.search import search_bp
from fms.routes.admin import admin_bp
from fms.routes.inventory import inventory_bp
from fms.routes.franchise_location import franchise_location_bp
from fms.routes.customer_preferences import preferences_bp
from fms.routes.sales import sales_bp

def register_routes(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(franchises_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(payments_bp)
    app.register_blueprint(finances_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(notification_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(browse_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(inventory_bp)
    app.register_blueprint(franchise_location_bp)
    app.register_blueprint(preferences_bp)
    app.register_blueprint(sales_bp)