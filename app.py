import os

from flask import Flask, render_template_string
from flask_security import Security, current_user, auth_required, hash_password, SQLAlchemySessionUserDatastore
from database import db_session, init_db
from models import User, Role

app = Flask(__name__)
app.config['DEBUG'] = True

# Generate a nice key using secrets.token_urlsafe()
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
# Bcrypt is set as default SECURITY_PASSWORD_HASH
# Generate a good salt using: secrets.SystemRandom().getrandbits(128)
app.config['SECURITY_PASSWORD_SALT'] = os.environ.get("SECURITY_PASSWORD_SALT")

# Setup Flask-Security
user_datastore = SQLAlchemySessionUserDatastore(db_session, User, Role)
security = Security(app, user_datastore)

# Create a user to test with
@app.before_first_request
def create_user():
    init_db()
    user_datastore.create_user(email="test@me.com", password=hash_password("password"))
    db_session.commit()

# Views
@app.route("/")
@auth_required()
def home():
    return render_template_string('Hello {{email}} !', email=current_user.email)

if __name__ == '__main__':
    app.run()