from models import app, User, socketio
from flask import jsonify, request


@app.route("/")
def home():
  return "Is this thing on?"

@socketio.on('message')
def handleMessage(msg):
  print('Message: ' + msg)
  send(msg, broadcast=True) 
  #broadcast=True means EVERYONE gets it
