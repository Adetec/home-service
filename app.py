#!/usr/bin/env python3

# Import modules
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Base, User
from flask import session as login_session

app = Flask(__name__)

# Connect to the database
engine = create_engine('sqlite:///data.db?check_same_thread=False')
# Create database session
DBsession = sessionmaker(bind=engine)
session = DBsession()


@app.route('/')
def home():
    return 'Home page'

@app.route('/admin')
def admin():
    admin = session.query(User).all()
    return 'My name is ' + admin[0].name + ' and I\'m ' + admin[0].m_type + ' here!' 



# Run the app in the '__main__' scope
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)