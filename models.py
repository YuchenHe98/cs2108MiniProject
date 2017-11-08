from app import db
from datetime import datetime


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    gender = db.Column(db.String(1))
    age = db.Column(db.Integer())
    description = db.Column(db.String(300))
    date = db.Column(db.DateTime, default = datetime.utcnow)

# get profile by id : Profile.query.get(id)
# get profile by param : Profile.query.filter_by(name = "").all()  


