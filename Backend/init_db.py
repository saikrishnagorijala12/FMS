from fms import db, create_app
from fms.models import *

app = create_app()

def create_db():
    with app.app_context():
        db.create_all()
        print('Database tables created successfully.')

create_db()
