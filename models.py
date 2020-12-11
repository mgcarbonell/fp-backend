import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from passlib.apps import custom_app_context as pwd_context
from flask_login import UserMixin
from flask_cors import CORS

app=Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config["SQLALCHEMY_DATABASE_URI"]= os.environ.get('DATABASE_URL')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
db = SQLAlchemy(app)
app.app_context().push()


class User(UserMixin, db.Model):
	__tablename__='users'

	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String, unique=True, nullable=False)
	username = db.Column(db.String, nullable=False) 
	password = db.Column(db.String, nullable=False)

	def __repr__(self):
		return f'User(id={self.id}, email={self.email}, name={self.name})'
	
	def as_dict(self):
		user_dict = {c.name: getattr(self, c.name) for c in self.__table__.columns}
		del user_dict['password']
		return user_dict

	def set_password(self, password):
		self.password = pwd_context.encrypt(password)

	def verify_password(self, typed_password):
		return pwd_context.verify(typed_password, self.password)

	def generate_token(self, expiration=60*10*10):
		s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
		return s.dumps({ 'id': self.id })

def get_or_create(model, defaults=None, **kwargs):
	instance = db.session.query(model).filter_by(**kwargs).first()
	if instance:
		return instance, False
	else:
		params = dict((k, v) for k, v in kwargs.items())
		params.update(defaults or {})
		instance = model(**params)
		db.session.add(instance)
		db.session.commit()
		return instance, True

db.create_all()