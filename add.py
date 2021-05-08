from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

class Add(db.Model):
    title = db.Column(db.String())
    prize = db.Column(db.Float())
    content = db.Column(db.String())
    added_date = db.Column(db.DateTime)
    real_estate_type = db.Column(db.String())
    room_number = db.Column(db.Integer)
    baths_number = db.Column(db.Integer)
    parking = db.Column(db.Boolean)
    size = db.Column(db.Float)
    location = db.Column(db.String())

    def __init__(self):
        self.title = title
        self.prize = prize
        self.content = content
        self.added_date = added_date
        self.real_estate_type = real_estate_type
        self.room_number = room_number
        self.baths_number = baths_number
        self.parking = parking
        self.size = size
        self.location = location

    
