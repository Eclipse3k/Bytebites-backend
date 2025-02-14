from . import db
from argon2 import PasswordHasher
from datetime import datetime
import pytz

madrid_tz = pytz.timezone('Europe/Madrid')
ph = PasswordHasher()

# Association table for followers
followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('followed_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(1024), nullable=False)
    
    # Profile information
    bio = db.Column(db.String(500))
    daily_calorie_goal = db.Column(db.Integer)
    weight = db.Column(db.Float)  # in kg
    height = db.Column(db.Float)  # in cm
    date_of_birth = db.Column(db.Date)
    joined_at = db.Column(db.DateTime, default=lambda: datetime.now(madrid_tz))
    
    # Profile picture URL (stored in frontend/CDN)
    profile_picture_url = db.Column(db.String(500))
    
    # Relationships
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic'
    )

    def set_password(self, password):
        self.password_hash = ph.hash(password)

    def check_password(self, password):
        try:
            return ph.verify(self.password_hash, password)
        except Exception:
            return False
    
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
    
    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
    
    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0
    
    def get_feed(self):
        """Get food logs from followed users and self."""
        followed = FoodLog.query.join(
            followers, (followers.c.followed_id == FoodLog.user_id)
        ).filter(followers.c.follower_id == self.id)
        
        own = FoodLog.query.filter_by(user_id=self.id)
        
        return followed.union(own).order_by(FoodLog.log_date.desc())
    
    @property
    def followers_count(self):
        return self.followers.count()
    
    @property
    def following_count(self):
        return self.followed.count()

class Food(db.Model):
    __tablename__ = 'foods'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    calories_per_100g = db.Column(db.Float, nullable=False)
    protein_per_100g = db.Column(db.Float)
    carbs_per_100g = db.Column(db.Float)
    fat_per_100g = db.Column(db.Float)
    usda_id = db.Column(db.String(20), unique=True)  # To store USDA FoodData Central ID

class FoodLog(db.Model):
    __tablename__ = 'food_logs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    food_id = db.Column(db.Integer, db.ForeignKey('foods.id'), nullable=False)
    grams = db.Column(db.Float, nullable=False)
    log_date = db.Column(db.DateTime, default=lambda: datetime.now(madrid_tz), index=True)

    user = db.relationship('User', backref='food_logs')
    food = db.relationship('Food', backref='food_logs')