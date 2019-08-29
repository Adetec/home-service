#!/usr/bin/env python3

# Import modules
from flask import Flask, render_template, url_for, request, redirect, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Base, User
from flask import session as login_session
from flask_bcrypt import Bcrypt
from forms import RegistrationForm, LoginForm
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_httpauth import HTTPBasicAuth
import smtplib
from email.message import EmailMessage
from wtforms.validators import ValidationError


auth = HTTPBasicAuth()


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Super_secret_key'
photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
configure_uploads(app, photos)

EMAIL_ADDRESS = 'adetech.home.service@gmail.com'
EMAIL_PASSWORD = 'uhelsctayopsytlq'

def send_activation_email(username, user_email, code):
    msg = EmailMessage()
    msg['Subject'] = 'Home service | Activate your account'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = user_email
    msg.set_content('Welcome ' + username + ' among us to HOME SERVICE APP. Please activate your account using this code: ' + code)
    msg.add_alternative('<div dir="rtl"><p> مرحبا بك <strong style="color:darkslateblue;">' + username + '</strong> في تطبيقنا المتواضع HOME SERVICE ،</p><p> يجب عليك تفعيل حسابك لللإستفادة من خدماتنا <strong style="color:darkslateblue;">' + code + '</strong></p></div>', subtype='html')
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:

        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        try:
            return smtp.send_message(msg)
        except:
            print('Email not sent')

# Connect to the database
engine = create_engine('sqlite:///data.db?check_same_thread=False')
# Create database session
DBsession = sessionmaker(bind=engine)
session = DBsession()

bcrypt = Bcrypt(app)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/admin')
def admin():
    users = session.query(User).all()
    return 'My name is ' + users[0].name + ' and I\'m ' + users[0].m_type + ' here!'


@app.route('/users')
# @auth.login_required
def display_users():
    users = session.query(User).all()
    return render_template('coucou.html', users=users)


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        username = form.username.data
        email = form.email.data
        password=form.password.data

        # Hash user password
        hashed_passowrd = bcrypt.generate_password_hash(password).decode('utf-8')
        if username is None or password is None:
            abort(400)
        user = User(
            name=username,
            email=request.form['email'],
            password=hashed_passowrd,
            m_type='admin')
        # Check register validation
        if form.validate_on_submit():
            try:
                session.add(user)
                session.commit()
                print(user.name + ' is added')
                send_activation_email(user.name, user.email, '1984')
                users = session.query(User).all()
                flash(f'{user.name} added')
                return (redirect(url_for('display_users')))
            except:
                print('Something went wrong')
        return render_template('register.html', form=form)
    else:
        return render_template('register.html', form=form)
