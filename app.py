import os
from flask import Flask, request, redirect, flash, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from process import get_matched_results
import models


APP_ROOT =  os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, "temp_upload/")
app = Flask(__name__)
app.config['APP_ROOT'] = APP_ROOT
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(APP_ROOT, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route('/index')
@app.route('/')

def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        target = app.config['UPLOAD_FOLDER']
        if  not os.path.isdir(target):
            os.mkdir(target)

        if 'file' not in request.files:
            flash('No file choosen')
            return redirect(request.url)

        file = request.files['file'] 

        if file.filename == '':
            flash('No file choosen')
            return redirect(request.url)

        if (file):
            filename = secure_filename('temp.jpg')
            destination = "/".join([app.config['UPLOAD_FOLDER'], filename])
            file.save(destination)

        # run matching and return matched results
        matched_profile_ids = get_matched_results(file)

        # for each id in matched id, get the profile object from db by id
        matched_profiles = [ models.Profile.query.get(id) for id in matched_profile_ids]

        return render_template('show.html', profiles = matched_profiles)

if __name__ == "__main__":
    app.run()
