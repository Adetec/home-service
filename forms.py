from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

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


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')