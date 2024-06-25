import json
import string
from functools import wraps
import random

from flask_login import current_user, login_required, login_user, logout_user
from flask_wtf import FlaskForm
from wtforms.fields import SubmitField
from wtforms.validators import DataRequired, ValidationError

from app import app
from app.models import User, Code, Question, Result, db
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
    return render_template('index.html')


@app.route('/7-class')
def class7():
    theme = request.args.get('theme')
    if theme:
        return render_template(f'7class/{theme}.html')
    return render_template('7class.html')


@app.route('/8-class')
def class8():
    theme = request.args.get('theme')
    if theme:
        return render_template(f'8class/{theme}.html')
    return render_template('8class.html')


@app.route('/9-class')
def class9():
    theme = request.args.get('theme')
    if theme:
        return render_template(f'9class/{theme}.html')
    return render_template('9class.html')


@app.route('/testCode', methods=['GET', 'POST'])
def codetest():
    if request.method == 'POST':
        code = request.form['code']
        if Code.query.filter_by(code=code).first():
            return redirect(url_for('quest'))
        else:
            flash('Код неверный')
        return redirect(url_for('codetest'))
    else:
        return render_template("testCode.html")


@app.route('/quest', methods=['GET', 'POST'])
def quest():
    if request.method == 'POST':
        FIO = request.form['FIO']
        cls = request.form['class']
        answrs = []
        for i in range(len(Question.query.all())):
            answrs.append(request.form[f'test{i+1}'])
        col = 0;
        print(Code.query.first().code)
        for i in range(len(answrs)):
            if answrs[i].lower() == Question.query.all()[i].answer.lower():
                col += 1
        res = Result(code=Code.query.first().code, name=FIO, user_class=cls, result=col, max=len(Question.query.all()))
        db.session.add(res)
        db.session.commit()
        return render_template('quest.html', answers=answrs, quests=Question.query.all())
    else:
        return render_template("quest.html", quests=Question.query.all())


@app.route('/result')
def result():
    codes = db.session.query(Result.code).distinct().all()
    names = {}
    results_ = {}
    for i in codes:
        namess = Result.query.filter_by(code=i.code).all()
        print(namess)
        names[i.code] = [nms.name for nms in namess]
        results_[i.code] = [nms.result for nms in namess]
    print(names, results_)
    return render_template("result.html", codes=codes, Result=Result, names=names, results=results_)

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
