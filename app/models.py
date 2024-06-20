from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
from sqlalchemy import MetaData

from app import app


convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(app, metadata=metadata)
migrate = Migrate(app, db, render_as_batch=True)

# Модель для ролей
class Role(db.Model, RoleMixin):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255))

# Модель для пользователей
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
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

class Theme(db.Model):
    __tablename__ = 'themes'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)

    def __repr__(self):
        return f'<Theme {self.name}>'

class Question(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    text = db.Column(db.Text(), unique=True, nullable=False)

    answer = db.Column(db.String(255))
    type = db.Column(db.Integer(), db.ForeignKey('qtypes.id'))
    theme_id = db.Column(db.Integer(), db.ForeignKey('themes.id'))

    def __repr__(self):
        return f'<Question {self.text}>'

class QType(db.Model):
    __tablename__ = 'qtypes'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)

    questions = db.relationship('Question', backref='qtype', lazy=True)

    def __repr__(self):
        return f'<QType {self.name}>'