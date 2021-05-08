from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import house_scraper
# from add import Add

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db = SQLAlchemy(app)
db.create_all()

class Add(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String())
    prize = db.Column(db.Float)
    content = db.Column(db.String())
    added_date = db.Column(db.DateTime)
    real_estate_type = db.Column(db.String())
    room_number = db.Column(db.Integer)
    baths_number = db.Column(db.Integer)
    parking = db.Column(db.Boolean)
    size = db.Column(db.Float)
    location = db.Column(db.String())

    # def __init__(self):
    #     self.id = id
    #     self.title = title
    #     self.prize = prize
    #     self.content = content
    #     self.added_date = added_date
    #     self.real_estate_type = real_estate_type
    #     self.room_number = room_number
    #     self.baths_number = baths_number
    #     self.parking = parking
    #     self.size = size
    #     self.location = location

@app.route('/', methods=['GET'])
def main():
    urls = house_scraper.get_urls()
    ads = house_scraper.scrape_add(urls)
    return jsonify(ads)


if __name__ == '__main__':
    app.run(debug=True)