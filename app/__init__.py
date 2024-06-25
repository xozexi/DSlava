from flask import Flask, redirect, url_for
from flask_admin import Admin, BaseView, expose
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.fields import QuerySelectField
from flask_login import LoginManager
from flask_security import SQLAlchemyUserDatastore, Security, current_user
from itsdangerous import URLSafeTimedSerializer
from sqlalchemy import desc
from wtforms.fields.choices import SelectField

from app.settings import app
from app.models import db, User, Role, Question, Theme, Code, Result


class AdminView(ModelView):
    column_display_pk = True  # Показывать первичный ключ в таблице
    can_view_details = True

    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('index'))


class HomeAdminView(AdminIndexView):
    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('index'))


class QuestionView(ModelView):
    form_overrides = {
        'theme_id': SelectField
    }
    form_args = {
        'theme_id': {
            'query_factory': lambda: db.session.query(Theme),
            'get_label': 'name'
        }
    }


admin = Admin(app, 'Назад', url='/', index_view=HomeAdminView())
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
admin.add_view(AdminView(Code, db.session, name='Коды Заданий'))
admin.add_view(AdminView(User, db.session, name='Пользователи'))
admin.add_view(AdminView(Role, db.session, name='Роли'))
admin.add_view(AdminView(Theme, db.session, name='Темы'))
admin.add_view(QuestionView(Question, db.session, name='Вопросы'))
admin.add_view(AdminView(Result, db.session, name='Результаты'))

security = Security(app, user_datastore)
