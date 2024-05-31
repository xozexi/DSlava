import json
import string
from functools import wraps
import random

from flask_login import current_user, login_required, login_user, logout_user
from flask_wtf import FlaskForm
from wtforms.fields import SubmitField
from wtforms.validators import DataRequired, ValidationError

from app import app
from app.models import User, Teacher, Administration, Workers
from flask import flash, redirect, render_template, request, url_for, jsonify
from sqlalchemy import or_, func, text, asc, desc

from app.settings import manager

from wtforms import Form, BooleanField, StringField, PasswordField, validators

manager.login_view = 'signin'


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('signin', next=request.url))
        return f(*args, **kwargs)

    return decorated_function


@app.route('/')
def index():
    admins = Administration.query.all()
    print(teachers)
    return render_template('index.html', admins=admins)


@app.route('/teachers')
def teachers():
    teacherss = Teacher.query.all()
    return render_template('teachers.html', teachers=teacherss)


@app.route('/workers')
def workers():
    workerss = Workers.query.all()
    return render_template('worker.html', workers=workerss)


@app.route('/info')
def info():
    id = request.args.get('id')
    type = request.args.get('type')
    info_data = None
    if type == 'Teacher':
        info_data = Teacher.query.filter_by(id=id).first()
    elif type == 'Workers':
        info_data = Workers.query.filter_by(id=id).first()
    elif type == 'Administration':
        info_data = Administration.query.filter_by(id=id).first()
    return render_template('info.html', info=info_data, type=type)


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        user = User.query.filter_by(username=login).first()
        if user is not None and user.password == password:
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Неверный логин или пароль')
            return redirect(url_for('signin'))
    return render_template('security/login_user.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
