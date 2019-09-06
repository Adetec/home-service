from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from application.models import User, Category, Service


class RegistrationForm(FlaskForm):
    username = StringField('اسم المستخدم',
                           validators=[DataRequired(), Length(min=2, max=20)])
    
    email = StringField('البريد الإلكتروني',
                        validators=[DataRequired(), Email()])
    password = PasswordField('كلمة السر', validators=[DataRequired()])
    confirm_password = PasswordField('تأكيد كلمة السر',
                                     validators=[DataRequired(), EqualTo('password')])
    user_type = SelectField('طبيعة الحساب', validators=[DataRequired()], choices=[(None, 'طبيعة الحساب'), ('client', 'زبون'), ('worker', 'مهني'), ('enterprener', 'مقاول'), ('company', 'شركة')])
    submit = SubmitField('تسجيل')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('عفوا، هذا الإسم قد تم اختياره، برجاء إختيار إسم آخر')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('عفوا، هذا البريد محجوز، برجاء إختيار بريدا آخر')

    

class LoginForm(FlaskForm):
    email = StringField('البريد الإلكتروني',
                        validators=[DataRequired(), Email()])
    password = PasswordField('كلمة السر', validators=[DataRequired()])
    remember = BooleanField('تذكرني')
    submit = SubmitField('تسجيل الدخول')


class UpdateProfileForm(FlaskForm):
    username = StringField('اسم المستخدم',
                           validators=[DataRequired(), Length(min=2, max=20)])
    full_name = StringField('الإسم الكامل',
                           validators=[Length(min=2, max=20)])
    picture = FileField('تحميل الصورة الشخصية', validators=[FileAllowed(['jpg', 'png'])])
    address_first_line = StringField('العنوان', validators=[])
    address_second_line = StringField('2العنوان', validators=[])
    city = StringField('الولاية', validators=[])
    submit = SubmitField('تعديل')

    def validate_username(self, username):
        if not username.data == current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('عفوا، هذا الإسم قد تم اختياره، برجاء إختيار إسم آخر')


class CategoryForm(FlaskForm):
    category_name = StringField('الصنف', validators=[DataRequired()])
    description = TextAreaField('وصف الصنف', validators=[DataRequired()])
    picture = FileField('تحميل صورة الصنف', validators=[FileAllowed(['jpg', 'png', 'svg'])])
    submit = SubmitField('إظافة')


class ServiceForm(FlaskForm):
    categories = Category.query.all()
    cat_ids = []
    for cat in categories:
        cat_ids.append((str(cat.id), cat.category_name))
    service_name = StringField('الخدمة', validators=[DataRequired()])
    description = TextAreaField('وصف الخدمة', validators=[DataRequired()])
    picture = FileField('تحميل صورة الخدمة', validators=[FileAllowed(['jpg', 'png', 'svg'])])
    category_id = SelectField('الصنف', validators=[], choices=cat_ids)
    submit = SubmitField('إظافة')


class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('ارسال الطلب')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('عذرا، لايوجد حساب مسجل لدينا بهذا البريد. أعد المحاولة من جديد')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')