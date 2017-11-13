import os
from flask import Flask
from database import db

APP_ROOT =  os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, "temp_upload/")
app = Flask(__name__)
app.config['APP_ROOT'] = APP_ROOT
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROFILE_PIC_LOCATION'] = os.path.join(APP_ROOT, 'profile_pictures')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(APP_ROOT, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.urandom(24)

db.init_app(app)

import routes

if __name__ == "__main__":
    app.run()
