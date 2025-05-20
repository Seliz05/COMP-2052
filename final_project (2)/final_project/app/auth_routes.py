from flask import Blueprint, render_template, redirect, url_for, flash
from app.forms import LoginForm, RegisterForm
from app.models import db, User, Role
from flask_login import login_user, logout_user, login_required

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        flash('Credenciales inválidas', 'danger')
    return render_template('login.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Buscar el rol seleccionado
        role = Role.query.filter_by(name=form.role.data).first()
        if not role:
            flash('Rol inválido seleccionado', 'danger')
            return redirect(url_for('auth.register'))

        user = User(
            username=form.username.data,
            email=form.email.data,
            role=role
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Usuario registrado exitosamente.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada correctamente.', 'info')
    return redirect(url_for('auth.login'))