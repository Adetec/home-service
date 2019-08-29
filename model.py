# Import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from passlib.apps import custom_app_context as pwd_context

Base = declarative_base()

# Create Needed models for database tables
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False, index=True)
    email = Column(String(250), nullable=False)
    m_type = Column(String(50), nullable=False)
    password = Column(String(64), nullable=False)
    image = Column(String(250), nullable=False, default='profile.jpg')
    '''
    def hash_password(self, password):
        self.password_hash = pwd_context.hash(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    '''
    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'm_type': self.m_type,
            'password': self.password,
            'image': self.image
        }


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    image = Column(String(100))
    # image = image_attachment('Picture')
    description = Column(String(2000))

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    # Method for API enpoints
    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'image': self.image,
            'description': self.description,
            'user_id': self.user_id
        }

'''
class UserPicture(Base, Image):
    __tablename__ = 'picture'

    user_id = Column(Integer, ForeignKey('category.id'), primary_key=True)
    user = relationship('Category')
 '''

engine = create_engine('sqlite:///data.db')
Base.metadata.create_all(engine)