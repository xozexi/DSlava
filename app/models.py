from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_security import UserMixin, RoleMixin
from app import app

db = SQLAlchemy(app)
migrate = Migrate(app, db)


# Модель для ролей (если вы еще не добавили ее в предыдущем примере)
class Role(db.Model, RoleMixin):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


# Модель для пользователей (если вы еще не добавили ее в предыдущем примере)
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    roles = db.relationship('Role', secondary='user_roles')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)


class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))


class Teacher(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(255))
    lastName = db.Column(db.String(255))
    midleName = db.Column(db.String(255))
    email = db.Column(db.String(255))
    address = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    data_start_work = db.Column(db.Date)
    info = db.Column(db.Text)
    inst = db.Column(db.String(255))
    telegram = db.Column(db.String(255))
    vk = db.Column(db.String(255))
    tiktok = db.Column(db.String(255))
    img = db.Column(db.Text)


class Administration(db.Model):
    __tablename__ = 'administration'
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(255))
    lastName = db.Column(db.String(255))
    midleName = db.Column(db.String(255))
    email = db.Column(db.String(255))
    address = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    data_start_work = db.Column(db.Date)
    info = db.Column(db.Text)
    inst = db.Column(db.String(255))
    telegram = db.Column(db.String(255))
    vk = db.Column(db.String(255))
    tiktok = db.Column(db.String(255))
    img = db.Column(db.Text)


class Workers(db.Model):
    __tablename__ = 'workers'
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(255))
    lastName = db.Column(db.String(255))
    midleName = db.Column(db.String(255))
    email = db.Column(db.String(255))
    address = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    data_start_work = db.Column(db.Date)
    info = db.Column(db.Text)
    inst = db.Column(db.String(255))
    telegram = db.Column(db.String(255))
    vk = db.Column(db.String(255))
    tiktok = db.Column(db.String(255))
    img = db.Column(db.Text)