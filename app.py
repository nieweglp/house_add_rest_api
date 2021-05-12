from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from house_scraper_gum_tree import get_urls, scrape_add



app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.config['JSON_AS_ASCII'] = False

PAGES = 2

db = SQLAlchemy(app)

class Add(db.Model):
    id = db.Column(db.String(), primary_key = True)
    title = db.Column(db.String())
    prize = db.Column(db.String())
    content = db.Column(db.String())
    added_date = db.Column(db.String())
    sold_by = db.Column(db.String())
    real_estate_type = db.Column(db.String())
    room_number = db.Column(db.String())
    baths_number = db.Column(db.String())
    parking = db.Column(db.String())
    size = db.Column(db.Integer())
    location = db.Column(db.String())
    def to_dict(self):
        return {'id': self.id, 'title': self.title, 'prize': self.prize,
                'content': self.content, 'added_date': self.added_date, 
                'sold_by': self.sold_by, 'real_estate_type': self.real_estate_type, 
                'room_number': self.room_number, 'baths_number': self.baths_number, 
                'parking': self.parking, 'size': self.size, 'location': self.location}


@app.route('/scrape')
def scrape():
    gum_tree_urls = get_urls(pages=PAGES)
    gum_tree_adds = scrape_add(gum_tree_urls)
    for add in gum_tree_adds:
        adds_to_db = Add(**add)
        db.session.add(adds_to_db)
        db.session.commit()
    return jsonify(gum_tree_adds)

@app.route('/data')
def load_data():
    all_adds = Add.query.all()
    all_adds_list = [add.to_dict() for add in all_adds]
    return jsonify(all_adds_list)

@app.route('/')
def main():
    return "Hello"


if __name__ == '__main__':
    app.run(debug=True)