from app import create_app, db
from app.models import User

app = create_app()
with app.app_context():
    db.create_all()  # This creates all tables defined in your models
    print("Tables created successfully!")