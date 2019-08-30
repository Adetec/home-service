from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from models import User

# Connect to the database
engine = create_engine('sqlite:///data.db?check_same_thread=False')
# Create database session
DBsession = sessionmaker(bind=engine)
session = DBsession()


class RegistrationForm(FlaskForm):
    username = StringField('الإسم',
                            validators=[DataRequired(), Length(min=2, max=250)])
    email = StringField('البريد الإلكتروني',
                        validators=[DataRequired(), Email()])
    password = PasswordField('كلمة السر', validators=[DataRequired()])
    confirm_password = PasswordField('تأكيد كلمة السر',
                                    validators=[DataRequired(), EqualTo('password')])
    picture = FileField('تحميل الصورة', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('تسجيل')

    def validate_email(self, email):
        user = session.query(User).filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')