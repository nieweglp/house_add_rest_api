from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import house_scraper
# from add import Add

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
# app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)

class Add(db.Model):
    id = db.Column(db.String(), primary_key = True)
    title = db.Column(db.String())
    # prize = db.Column(db.String())
    # content = db.Column(db.String())
    # added_date = db.Column(db.String())
    # real_estate_type = db.Column(db.String())
    # room_number = db.Column(db.String())
    # baths_number = db.Column(db.String())
    # parking = db.Column(db.String())
    # size = db.Column(db.String())
    # location = db.Column(db.String())
    def to_dict(self):
        return {'id': self.id, 'title': self.title}


@app.route('/scrape')
def scrape():
    urls = house_scraper.get_urls(pages=2)
    adds = house_scraper.scrape_add(urls)
    for add in adds:
        adds_to_db = Add(**add)
        db.session.add(adds_to_db)
        db.session.commit()
    return jsonify(adds)

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