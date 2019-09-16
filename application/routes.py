# Import modules
import os
import secrets
from datetime import datetime
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, jsonify
from application import app, db, bcrypt, mail
from application.forms import (RegistrationForm, LoginForm, UpdateProfileForm, CategoryForm,
ServiceForm, RequestResetForm, ResetPasswordForm, ServiceRequestMessagesForm, EmailVerificationForm)
from application.models import User, Category, Service, ServiceRequest, ServiceRequestMessages
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message



@app.route("/")
@app.route("/home")
def home():
    categories = Category.query.all()
    services = Service.query.all()
    return render_template('home.html', categories=categories, services=services, title='Need Help!')


def send_verification_email(user):
    token = user.get_reset_token(30000)
    
    msg = Message(
        f'مرحبا {user.username} في بيتك للخدمات',
        sender='adetech.home.service@gmail.com',
        recipients=[user.email],
    )
    msg.html = f'''
    <div dir="rtl">
    <h3>مرحبا <strong>{user.username}</strong></h3>
    <p>بناء على تسجيلكم في موقعنا بيتي للخدمات، نريد منكم تأكيد بريدكم الإلكتروني من أجل تفعيل حسابكم والإستفادة من خدماتنا </p>
    <p> يمكنكم فعل ذلك بالضغط من  <a href="{url_for('email_verification', token=token, _external=True)}" target="_BLANK">هنا</a></p>
    <p>إذا لم تقم بذلك، برجاء تجاهل هذه الرسالة</p>
    </div>
    '''
    try:
        mail.send(msg)
    except:
        print('Error encured while sending a verification email! ')




@app.route("/register", methods=['GET', 'POST'])
def register():
    categories = Category.query.all()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, user_type=form.user_type.data)
        db.session.add(user)
        db.session.commit()
        flash('قد تم تسجيلك بنجاح، برجاء تفقد بريدك الالكتروني', 'success')
        send_verification_email(user)
        return redirect(url_for('login'))
    return render_template('register.html', categories=categories, form=form, title='NH | حساب جديد')


@app.route('/email_verification/<token>', methods=['GET', 'POST'])
def email_verification(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if not user:
        flash('طلب التفعيل غير صحيح أو قد انتهت صلاحيته', 'warning')
        return redirect(url_for('reset_request'))
    form = EmailVerificationForm()
    if form.validate_on_submit():
        
        user.is_active = True
        db.session.commit()
        flash('قد تم تفعيل حسابك بنجاح', 'success')
        return redirect(url_for('login'))
    return render_template('email-verification.html', form=form, title='NH | تفعيل الحساب')


@app.route("/login", methods=['GET', 'POST'])
def login():
    categories = Category.query.all()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            if not user.is_active:
                flash('حسابك ليس مفعل بعد، تفقد بريدك الإلكتروني من أجل تفعيل حسابك', 'info')
                send_verification_email(user)
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            user.last_login = datetime.now()
            user.is_connected = True
            db.session.commit()
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('الرجاء التأكد من بريدك الإلكتروني أو كلمة السر', 'danger')
    return render_template('login.html', categories=categories, form=form, title='NH | تسجيل دخول')


@app.route("/logout")
def logout():
    user = current_user
    user.is_connected = False
    db.session.commit()
    logout_user()
    return redirect(url_for('home'))

@app.route('/users')
# @auth.login_required
def display_users():
    users = User.query.all()
    categories = Category.query.all()
    return render_template('users.html', users=users, categories=categories, title='NH | المستخدمين')

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
    picture_filname = f'{hex_random}{file_extension}'
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
    categories = Category.query.all()
    services = Service.query.all()   
    form = UpdateProfileForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_profile_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.full_name = form.full_name.data
        current_user.address_first_line = form.address_first_line.data
        current_user.address_second_line = form.address_second_line.data
        current_user.city = form.city.data
        db.session.commit()
        flash('قد تم تعديل معلوماتك بنجاح', 'success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        n_requests = len(current_user.requests)
        n_services = len(current_user.services)
        form.username.data = current_user.username
        form.full_name.data = current_user.full_name
        form.address_first_line.data = current_user.address_first_line
        form.address_second_line.data = current_user.address_second_line
        form.city.data = current_user.city
    return render_template('profile.html', form=form, n_services=n_services, n_requests=n_requests, categories=categories, services=services, title='NH | حسابي')


def send_reset_email(user):
    token = user.get_reset_token(30000)
    # '<div dir="rtl"><p> مرحبا بك <strong style="color:darkslateblue;">' + username + '</strong> في تطبيقنا المتواضع HOME SERVICE ،</p><p> يجب عليك تفعيل حسابك لللإستفادة من خدماتنا <strong style="color:darkslateblue;">' + code + '</strong></p></div>', subtype='html'
    msg = Message(
        'تغيير كلمة المرور',
        sender='adetech.home.service@gmail.com',
        recipients=[user.email],
    )
    msg.html = f'''
    <div dir="rtl">
    <h3>مرحبا <strong>{user.username}</strong></h3>
    <p>بناءعلى طلبك بتغيير كلمة المرور، يمكنكم فعل ذلك من <a href="{url_for('reset_token', token=token, _external=True)}" target="_BLANK">هنا</a></p>
    <p>إذا لم تقم بذلك، برجاء تجاهل هذه الرسالة</p>
    </div>
    '''
    try:
        mail.send(msg)
    except:
        print('Error encured while sendin a reset email! ')


def send_request_message(reciever, service, message, client_id, service_id):
    user_sender = User.query.get(service.user_id)
    msg = Message(
        f'{user_sender.username} قد رد عليك',
        sender='adetech.home.service@gmail.com',
        recipients=[reciever.email],
    )
    msg.html = f'''
    <div style="padding:4px; font-size:1.3em; border:1px #17a2b8 solid;" dir="rtl">
        <h3>مرحبا <strong style="color:#007bff;">{reciever.username}</strong></h3>
        <p><strong>{user_sender.username}</strong> قد رد عليك فيما يخص بطلبك حول <strong style="color:#007bff;">{service.service_name}</strong></p>
        <p id="message" style="color:#17a2b8;">{message}</p>
        <p>يمكنك التواصل معه أو الرد عليه من <a href="{(url_for('request_service', client_id=client_id, service_id=service_id, _external=True))}" target="_BLANK">هنا</a></p>
    </div>
    '''

    try:
        mail.send(msg)
        flash(f'قد تم تبليغ {reciever.username} عبر البريد الالكتروني، برجاء إنتظار رده.', 'success')
    except:
        print('Error encured while sending the email! ')


def send_service_request_email(client, service, message, client_id, service_id):
    user_sender = User.query.get(client.id)
    msg = Message(
        f'{user_sender.username} لديك زبون جديد',
        sender='adetech.home.service@gmail.com',
        recipients=[service.owner.email],
    )
    msg.html = f'''
    <div style="padding:4px; font-size:1.3em; border:1px #17a2b8 solid;" dir="rtl">
        <h3>مرحبا <strong style="color:#007bff;">{service.owner.username}</strong></h3>
        <p><strong>{user_sender.username}</strong> مهتم بالخدمة المقدمة من طرفكم: <strong style="color:#007bff;">{service.service_name}</strong></p>
        <p style="color:#17a2b8;">{message.message}</p>
        <p>يمكنك التواصل معه أو الرد عليه من <a href="{(url_for('request_service', client_id=client_id, service_id=service_id, _external=True))}" target="_BLANK">هنا</a></p>
    </div>
    '''

    try:
        mail.send(msg)
        flash(f'قد تم تبليغ {service.owner.username} عبر البريد الالكتروني، برجاء إنتظار رده.', 'success')
    except:
        print('Error encured while sending the email! ')


@app.route('/reset_request', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('قد تم إرسال تعليمات إعادة تغيير كلمة المرور، برجاء تفقد بريدك', 'info')
        return redirect(url_for('home'))
    return render_template('reset-request.html', form=form, title='NH | طلب تغيير كلمة المرور')


@app.route('/reset_token/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if not user:
        flash('الطلب غير صحيح أو قد انتهت صلاحيته', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('قد تم تغيير كلمة المرور بنجاح', 'success')
        return redirect(url_for('login'))
    return render_template('reset-token.html', form=form, title='NH | تغيير كلمة المرور')


# Category routes:
@app.route('/category/new', methods=['GET', 'POST'])
def add_category():
    categories = Category.query.all()
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(category_name=form.category_name.data, description=form.description.data)
        if form.picture.data:
            picture_file = save_picture(form.picture.data, 'categories')
            category.image_file = picture_file
        db.session.add(category)
        db.session.commit()
        flash('قد تم إظافة الصنف بنجاح', 'success')
        return redirect(url_for('home'))
    return render_template('new-category.html', form=form, categories=categories, title='NH | صنف جديد')

@app.route('/category/<int:id>')
def category_details(id):
    categories = Category.query.all()
    category = Category.query.get_or_404(id)

    return render_template('category.html', categories=categories, category=category)

@app.route('/category/<int:id>/update', methods=['GET', 'POST'])
def update_category(id):
    categories = Category.query.all()
    category = Category.query.filter_by(id=id).first()
    if not current_user.is_authenticated:
        return redirect(url_for('home'))
    elif not current_user.user_type == 'admin':
        flash('عذرا لست مصرحا لتعديل هذا الصنف', 'danger')
        return redirect(url_for('home'))
    form = CategoryForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data, 'categories')
            category.image_file = picture_file
        category.category_name = form.category_name.data
        category.description = form.description.data
        db.session.commit()
        flash('قد تم تحديث الصنف بنجاح', 'success')
        return redirect(url_for('home'))
    elif request.method == 'GET':
        form.category_name.data = category.category_name
        form.description.data = category.description
    return render_template('new-category.html', form=form, categories=categories, title='NH | تفيير الصنف')



# Service routes:
@app.route('/service/<int:id>')
def service_details(id):
    categories = Category.query.all()
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    service = Service.query.get_or_404(id)

    return render_template('service.html', categories=categories, service=service)


@app.route('/service/new', methods=['GET', 'POST'])
def add_service():
    categories = Category.query.all()
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    form = ServiceForm()
    print(form.category_id.data)
    if form.validate_on_submit():
        category = Category.query.filter_by(id=int(form.category_id.data))
        service = Service(service_name=form.service_name.data, description=form.description.data, category_id=form.category_id.data, owner=current_user)
        if form.picture.data:
            picture_file = save_picture(form.picture.data, 'services')
            service.image_file = picture_file
        db.session.add(service)
        db.session.commit()
        flash('قد تم إظافة الخدمة بنجاح', 'success')
        return redirect(url_for('home'))
    return render_template('new-service.html', form=form, categories=categories, title='NH | خدمة جديدة')


@app.route('/service/<int:id>/update', methods=['GET', 'POST'])
def update_service(id):
    service = Service.query.filter_by(id=id).first()
    categories = Category.query.all()
    if not current_user.is_authenticated:
        return redirect(url_for('home'))
    elif not current_user.id == service.user_id:
        flash('عذرا لست مصرحا لتعديل هذه الخدمة', 'danger')
        return redirect(url_for('home'))
    form = ServiceForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data, 'services')
            service.image_file = picture_file
        service.service_name = form.service_name.data
        service.description = form.description.data
        service.description = form.description.data
        service.category_id = form.category_id.data
        db.session.commit()
        flash('قد تم تحديث الخدمة بنجاح', 'success')
        return redirect(url_for('home'))
    elif request.method == 'GET':
        form.service_name.data = service.service_name
        form.description.data = service.description
        form.category_id.data = service.category_id
    return render_template('new-service.html', form=form, categories=categories, title='NH | تفيير الخدمة')


@app.route('/request_service/<int:client_id>/<int:service_id>/new', methods=['GET', 'POST'])
def request_service(client_id, service_id):
    categories = Category.query.all()
    if not current_user.is_authenticated:
        return redirect(url_for('home'))
    service = Service.query.get(service_id)
    print(f'test: current user: {current_user.id} => client: {client_id} => service user: {service.user_id}')
    if (current_user.id != client_id) and (current_user.id != service.user_id) :
        flash('لايمكنك التوقب على أمور الناس', 'warning')
        return redirect(url_for('home'))
    form = ServiceRequestMessagesForm()
    sender = current_user.id
    if form.validate_on_submit():
        service_request = ServiceRequest.query.filter_by(service_id=service_id).first()
        print(service_request)
        client = User.query.get(client_id)
        if not service_request:
            service_request = ServiceRequest(client_id=client_id, service_id=service_id)
            db.session.add(service_request)
            db.session.commit()
            message = ServiceRequestMessages(service_request_id=service_request.id, sender=sender, message=form.message.data)
            db.session.add(message)
            db.session.commit()
            send_service_request_email(client, service, message, client_id, service_id)
        else:
            service_request = ServiceRequest.query.filter_by(service_id=service_id).first()
            message = ServiceRequestMessages(service_request_id=service_request.id, sender=sender, message=form.message.data)
            db.session.add(message)
            db.session.commit()
        if sender == service.user_id:
            send_request_message(client, service, message.message, client_id, service_id)
        return redirect(url_for('request_service', client_id=client_id, service_id=service_id))
    service_request = ServiceRequest.query.filter_by(service_id=service_id).first()
    
    client = User.query.get(client_id)
    return render_template('request-service.html', client=client, service=service, form=form, service_request=service_request, categories=categories, title='NH | التواصل مع مقدم الخدمة')



'''
    * * * * * * * * * * *
    *   API EndPoints   *
    * * * * * * * * * * *
'''

@app.route('/API/1.0')
def home_endpoint():
    users = User.query.all()
    categories = db.session.query(Category).all()
    services = db.session.query(Service).all()
        
    u = []
    c = []
    s = []
    for user in users:
        u.append(user.serialize)
    for category in categories:
        c.append(category.serialize)
    for service in services:
        s.append(service.serialize)
    return jsonify(users=u, categories=c, services=s)
