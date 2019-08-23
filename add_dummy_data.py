# Import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# Import models
from model import Base, User
import sys

# Connect to the database and create a session
engine = create_engine('sqlite:///data.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create default user
admin = User(name='Adel Lassag',
             email='adetech.aadl@gmail.com',
             m_type='admin',
             gender='male')
# save user to the database
try:
    session.add(admin)
    session.commit()
    print('The admin ' + admin.name + ' added to the database')
except exceptions.SQLAlchemyError:
    sys.exit('Encountered general SQLAlchemyError!')
