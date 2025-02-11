from . import db
from argon2 import PasswordHasher

ph = PasswordHasher()

class User(db.Model):
    __tablename__ = 'users'  # explicitly set a table name
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(1024), nullable=False)  # Increased size for Argon2

    def set_password(self, password):
        self.password_hash = ph.hash(password)

    def check_password(self, password):
        try:
            return ph.verify(self.password_hash, password)
        except Exception:
            return False