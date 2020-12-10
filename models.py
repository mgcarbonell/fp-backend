from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///countzero' #dotenv will need to go here.
app.config['SECRET_KEY'] = 'placeholder' #dotenv will need to go here.
db = SQLAlchemy(app)

class User(db.Model):
  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String, unique=True, nullable=False)
  name = db.Column(db.String, nullable=False)
  password = db.Column(db.String, nullable=False)
  bio = db.Column(db.String(150))

  def __repr__(self):
      return f'User(id={self.id}, email="{self.email}", name="{self.name}")'
