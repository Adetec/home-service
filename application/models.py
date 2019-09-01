# Import modules
from datetime import datetime
from application import db, login_manager
from flask_login import UserMixin

# Load logged user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    full_name = db.Column(db.String(64), default='no full name')
    email = db.Column(db.String(120), unique=True, nullable=False)
    user_type = db.Column(db.String(20))
    # Default Image credit is licensed by CC BY 3.0 "https://www.onlinewebfonts.com/icon/191958"
    image_file = db.Column(db.String(20), nullable=False, default='profile.svg')
    password = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

    # Method for API enpoints
    @property
    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'full_name': self.full_name,
            'email': self.email,
            'user_type': self.user_type,
            'password': self.password,
            'image_file': self.image_file
        }

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.Text)
    image_file = db.Column(db.String(20), nullable=False, default='profile.svg')

    def __repr__(self):
        return f"Category('{self.category_name}', '{self.id}', '{self.image_file}')"

    # Method for API enpoints
    @property
    def serialize(self):
        return {
            'id': self.id,
            'category_name': self.category_name,
            'description': self.description,
            'image_file': self.image_file
        }
db.create_all()