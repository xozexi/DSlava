from flask import Flask, redirect, url_for
from flask_admin import Admin, BaseView, expose
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager
from flask_security import SQLAlchemyUserDatastore, Security, current_user
from itsdangerous import URLSafeTimedSerializer
from sqlalchemy import desc

from app.settings import app
from app.models import db, User, Role, Teacher, Administration, Workers


class AdminView(ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('index'))


class HomeAdminView(AdminIndexView):
    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('index'))


admin = Admin(app, 'Назад', url='/', index_view=HomeAdminView(), template_mode='bootstrap4')
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
admin.add_view(AdminView(User, db.session, name='Пользователи'))
admin.add_view(AdminView(Teacher, db.session, name='Учителя'))
admin.add_view(AdminView(Administration, db.session, name='Администрация'))
admin.add_view(AdminView(Workers, db.session, name='Работники'))
security = Security(app, user_datastore)
