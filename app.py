#!/usr/bin/env python3

from flask import jsonify, request
from models import app, User
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from flask_httpauth import HTTPTokenAuth
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO, emit
from crud.user_crud import (
    get_user, create_user, update_user, destroy_user
)

app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app, resources={
    r'/*': {
        'origins': '*'
    }
})

auth = HTTPTokenAuth('Bearer')

socketio = SocketIO(app)

# Errors
@app.errorhandler(Exception)
def unhandled_exception(e):
    app.logger.error(f'Unhandled Exception: {e}')
    message_str = e.__str__()
    return jsonify(message=message_str.split(':')[0])

# Auth
@auth.verify_token
def verify_token(token):
  s = Serializer(app.config['SECRET_KEY'])
  try:
    data = s.loads(token)
    g.user = User.query.filter_by(id=data[id]).first()
  except SignatureExpired:
    print("ERROR: signature expired!")
    return False
  except BadSignature:
    print("Error: invalid signature!")
    return False
  return True

# User routes
@app.route('/auth/login', methods=['POST'])
def login():
  if request.json['email'] is None or request.json['password'] is None:
    raise KeyError('Email and Password is required.')

  user = User.query.filter_by(email=request.json['email']).first() #find first entry of the email

  if not user or not user.verify_password(request.json['password']):
    raise Exception("Unauthorized.")

  g.user = user
  token = user.generate_token()
  return jsonify(user=user.as_dict(), token=token.decode('ascii'), status_code=200)

@app.route('/auth/register', methods=['POST'])
def register():
  return create_user(**request.json)

@app.route('/users/<int:id>')
def user_get_one(id):
  return get_user(id)

@app.route('/profile/<int:user_id>', methods=['GET', 'POST', 'PUT'])
@auth.login_required #require a user to be logged in, use with socket routes
def profile(user_id):
  if request.method == 'GET':
    return get_user(id)
  elif request.method == 'PUT':
    return update_user(id, **request.get_json())
  elif request.method == 'DELETE':
    return destroy_user(id)

# routes
@app.route('/')
def home():
  return

# Socket routes

@socketio.on('connect')
# @auth.login_required omitting for now for test connections
def test_connect():
  emit('after connect', {'data':'Lets dance'})

@socketio.on('message')
def handleMessage(msg):
  print('Message: ' + msg)
  send(msg, broadcast=True)

if __name__ == '__main__':
  socketio.run(app)