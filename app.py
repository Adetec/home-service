#!/usr/bin/env python3

# Import modules
from flask import Flask, render_template, url_for, request, redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Base, User
from flask import session as login_session
from flask_uploads import UploadSet, configure_uploads, IMAGES


app = Flask(__name__)
photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
configure_uploads(app, photos)

# Connect to the database
engine = create_engine('sqlite:///data.db?check_same_thread=False')
# Create database session
DBsession = sessionmaker(bind=engine)
session = DBsession()


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/admin')
def admin():
    users = session.query(User).all()
    return 'My name is ' + users[0].name + ' and I\'m ' + users[0].m_type + ' here!'

@app.route('/users')
def display_users():
    users = session.query(User).all()
    return render_template('coucou.html', users=users)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        filename = photos.save(request.files['file'])
        password=request.form['password']
        username = request.form['name']
        if username is None or password is None:
            abort(400)
        user = User(
            name=username,
            email=request.form['email'],
            image=filename,
            m_type='admin')

        user.hash_password(password)
        print(user.name, user.password_hash)
        try:
            session.add(user)
            session.commit()
            print(user.name + ' is added')
        except:
            print('Something went wrong')
        users = session.query(User).all()
        return (redirect(url_for('display_users')))
    else:
        return (render_template('sign-up.html'))
        

# Run the app in the '__main__' scope
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)