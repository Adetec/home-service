# Import modules
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from application import db, login_manager, app
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
    services = db.relationship('Service', backref='owner', lazy=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    is_connected = db.Column(db.Boolean, default=False)
    address_first_line = db.Column(db.String(64), default='')
    address_second_line = db.Column(db.String(64), default='')
    city = db.Column(db.String(20), default='')
    lat = db.Column(db.Float(20))
    lon = db.Column(db.Float(20))
    requests = db.relationship('ServiceRequest', backref='client', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
    
    
    # Methods for reseting user password
    def get_reset_token(self, time_expires):
        s = Serializer(app.config['SECRET_KEY'], time_expires)
        return s.dumps({'user_id': self.id}).decode('utf-8')
    
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            User_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(User_id)


    # Method for API enpoints
    @property
    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'full_name': self.full_name,
            'email': self.email,
            'user_type': self.user_type,
            'created_at': self.created_at,
            'last_login': self.last_login,
            'address_first_line': self.address_first_line,
            'address_second_line': self.address_second_line,
            'city': self.city,
            'lat': self.lat,
            'lon': self.lon,
            'password': self.password,
            'image_file': self.image_file,
            'is_connected': self.is_connected
        }

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.Text)
    image_file = db.Column(db.String(20), nullable=False, default='category.svg')
    services = db.relationship('Service', backref='parent', lazy=True)

    def __repr__(self):
        return f"Category('{self.category_name}', '{self.id}', '{self.image_file}')"

    # Method for API enpoints
    @property
    def serialize(self):
        return {
            'id': self.id,
            'category_name': self.category_name,
            'description': self.description,
            'image_file': self.image_file,
        }


class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.Text)
    image_file = db.Column(db.String(20), nullable=False, default='profile.svg')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    requests = db.relationship('ServiceRequest', backref='requested', lazy=True)

    def __repr__(self):
        return f"Service('{self.service_name}', '{self.id}', '{self.image_file}')"

    # Method for API enpoints
    @property
    def serialize(self):
        return {
            'id': self.id,
            'service_name': self.service_name,
            'description': self.description,
            'user_id': self.user_id,
            'category_id': self.category_id,
            'image_file': self.image_file
        }


class ServiceRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    requested_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    messages = db.relationship('ServiceRequestMessages', backref='discussion', lazy=True)

    def __repr__(self):
        return f"RequestService('{self.id}', '{self.service_id}', '{self.client_id}')"
    
    @property
    def serialize(self):
        return {
            'id': self.id,
            'client_id': self.client_id,
            'service_id': self.service_id,
            'requested_at': self.requested_at
        }


class ServiceRequestMessages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_request_id = db.Column(db.Integer, db.ForeignKey('service_request.id'), nullable=False)
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"ServiceRequestMessages('{self.id}', '{self.service_request_id}', '{self.message}', '{self.created_at}')"
    
    @property
    def serialize(self):
        return {
            'id': self.id,
            'service_request_id': self.service_request_id,
            'message': self.message,
            'created_at': self.created_at
        }





db.create_all()