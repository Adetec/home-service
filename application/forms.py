from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from application.models import User, Category


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
    submit = SubmitField('تعديل')

    def validate_username(self, username):
        if not username.data == current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('عفوا، هذا الإسم قد تم اختياره، برجاء إختيار إسم آخر')


class CategoryForm(FlaskForm):
    cat_name = StringField('الصنف', validators=[DataRequired()])
    description = TextAreaField('وصف الصنف', validators=[DataRequired()])
    picture = FileField('تحميل صورة الصنف', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('إظافة')

    def validate_category_name(self, category_name):
        category = category.query.filter_by(category_name=category_name.data).first()
        if category:
            raise ValidationError('عفوا، هذا الصنف قد تم اختياره، برجاء إختيار صنف آخر')