from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, current_user
from core.views.auth.forms import LoginForm, SignupForm
from core.url_endpoint import redirect_dest
from core.models import User
from core import db, bcrypt

auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    # If user is already authenticated redirect to designated page
    if current_user.is_authenticated and current_user.role == 'admin':
        return redirect_dest(fallback=url_for('admin.dashboard'))
    elif current_user.is_authenticated and current_user.role == 'user':
        return redirect_dest(fallback=url_for('user.dashboard'))

    form = LoginForm()

    if request.method == 'POST' and form.validate():
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password) and user.role == 'admin':
            login_user(user, remember=form.remember.data)
            return redirect_dest(fallback=url_for('admin.dashboard'))
        elif user and bcrypt.check_password_hash(user.password, password) and user.role == 'user':
            login_user(user, remember=form.remember.data)
            return redirect_dest(fallback=url_for('user.dashboard'))
        else:
            flash('Login failed! Your email or password is incorrect.', 'danger')
    return render_template('login.html', form=form)


@auth_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    # If user is already authenticated redirect to designated page
    if current_user.is_authenticated and current_user.role == 'admin':
        return redirect_dest(fallback=url_for('admin.dashboard'))
    elif current_user.is_authenticated and current_user.role == 'user':
        return redirect_dest(fallback=url_for('user.dashboard'))

    form = SignupForm()

    if request.method == 'POST' and form.validate():
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = 'user'

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(name=name, email=email, password=hashed_password, role=role)

        db.session.add(user)
        db.session.commit()

        flash('Success! Your account has been created.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('signup.html', form=form)


@auth_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
