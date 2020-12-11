from flask import jsonify, redirect, g
from models import db, User

def error(err_locale, error):
  print("ERROR in", err_locale, ":", error)
  return jsonify(error=f'Server Error in {err_locale}', message=f'Server Error in {err_locale}')

def get_user(id):
  user = User.query.get(id)
  if user:
    return jsonify(user.as_dict())
  else:
    raise Exception(f'No user at id: {id}')

def create_user(**kwargs):
  username=kwargs['username']
  email=kwargs['email']
  password=kwargs['password']
  if not username or not email or not password:
    raise Exception('Username, email, and password are requried.')
  if User.query.filter_by(email=email).first() is not None:
    raise Exception('Please enter a unique username or email.')
  new_user = User(**kwargs)
  new_user.set_password(password)
  db.session.add(new_user)
  db.session.commit()
  g.user = new_user
  token = new_user.generate_token()
  return jsonify(user=new_user.as_dict(), token=token.decode('ascii'))

def update_user(id, username, email, password):
  try:
    user = User.query.get(id)
    if user:
      user.email = email or user.email
      user.username = username or user.username
      user.password = password or user.password
      db.session.commit()
      return jsonify(user.as_dict())
    else:
      return jsonify(f'Error finding user at {id}.')
  except Exception as error:
    return ('Updating a user', error)

def destroy_user(id):
  user = User.query.get(id)
  if user:
    db.session.delete(user)
    db.session.commit()
    return redirect('/')
  else:
    raise Exception(f'No user at id: {id}.')