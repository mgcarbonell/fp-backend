from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

@app.route("/")
def home():
  return "Is this thing on?"

if __name__ == "__main__":
  app.run()