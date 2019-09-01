# Import modules
import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from application import app, db, bcrypt
from application.forms import RegistrationForm, LoginForm, UpdateProfileForm, CategoryForm
from application.models import User, Category
from flask_login import login_user, current_user, logout_user, login_required



@app.route("/")
@app.route("/home")
def home():
    categories = Category.query.all()
    return render_template('home.html', categories=categories, title='Need Help!')




@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        print('cool')
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, user_type=form.user_type.data)
        db.session.add(user)
        db.session.commit()
        flash('قد تم تسجيلك بنجاح', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form, title='NH | حساب جديد')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('الرجاء التأكد من بريدك الإلكتروني أو كلمة السر', 'danger')
    return render_template('login.html', form=form, title='NH | تسجيل دخول')


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/users')
# @auth.login_required
def display_users():
    users = User.query.all()
    return render_template('users.html', users=users, title='NH | المستخدمين')

def save_profile_picture(picture_from_form):
    # Generate hex picture filename
    hex_random = secrets.token_hex(8)
    _ , file_extension = os.path.splitext(picture_from_form.filename)
    picture_filname = f'profile-{hex_random}{file_extension}'
    # Set the picture path
    picture_path = os.path.join(app.root_path, 'static/img/users-profile', picture_filname)
    print(f'Picture path: {picture_path}')
    # resize the picture
    output_size = (256, 256)
    image = Image.open(picture_from_form)
    image.thumbnail(output_size)
    # Finally Save it
    image.save(picture_path)

    return picture_filname


def save_picture(picture_from_form, folder):
    # Generate hex picture filename
    hex_random = secrets.token_hex(8)
    _ , file_extension = os.path.splitext(picture_from_form.filename)
    picture_filname = f'profil{hex_random}{file_extension}'
    # Set the picture path
    picture_path = os.path.join(app.root_path, f'static/img/{folder}', picture_filname)
    print(f'Picture path: {picture_path}')
    # resize the picture
    # output_size = (256, 256)
    # image = Image.open(picture_from_form)
    # image.thumbnail(output_size)
    # Finally Save it
    picture_from_form.save(picture_path)

    return picture_filname

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_profile_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.full_name = form.full_name.data
        db.session.commit()
        flash('قد تم تعديل معلوماتك بنجاح')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.full_name.data = current_user.full_name
    return render_template('profile.html', form=form, title='NH | حسابي')


# Category routes:
@app.route('/category/new', methods=['GET', 'POST'])
def add_category():
    if not current_user.is_authenticated:
        return redirect(url_for('home'))
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(category_name=form.category_name.data, description=form.description.data)
        if form.picture.data:
            picture_file = save_picture(form.picture.data, 'categories')
            category.image_file = picture_file
        db.session.add(category)
        db.session.commit()
        flash('قد تم إظافة الصنف بنجاح', 'success')
        return redirect(url_for('login'))
    return render_template('new-category.html', form=form, title='NH | صنف جديد')