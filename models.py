
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

app = Flask(__name__)
db = SQLAlchemy(app)

class Venue(db.Model):
  __tablename__ = 'venue'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  city = db.Column(db.String(120))
  state = db.Column(db.String(120))
  address = db.Column(db.String(120))
  phone = db.Column(db.String(120))
  genres = db.Column(db.ARRAY(db.String()))
  image_link = db.Column(db.String(500))
  facebook_link = db.Column(db.String(120))

  # TODO DONE: implement any missing fields, as a database migration using Flask-Migrate
  website = db.Column(db.String(120))
  seeking_talent = db.Column(db.Boolean)
  seeking_description = db.Column(db.String(500))
  shows = db.relationship('Shows', backref=db.backref('venue', lazy=True))
  area_id = db.Column(db.Integer, db.ForeignKey('area.id'), nullable=False) #redundant with city and state, only for /venues.html

class Artist(db.Model):
  __tablename__ = 'artist'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  city = db.Column(db.String(120))
  state = db.Column(db.String(120))
  phone = db.Column(db.String(120))
  genres = db.Column(db.ARRAY(db.String()))
  image_link = db.Column(db.String(500))
  facebook_link = db.Column(db.String(120))

  # TODO DONE: implement any missing fields, as a database migration using Flask-Migrate
  website = db.Column(db.String)
  seeking_venue = db.Column(db.Boolean)
  seeking_description = db.Column(db.String)
  shows = db.relationship('Shows', backref=db.backref('artist', lazy=True))


# TODO DONE Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#Shows
class Shows(db.Model):
  __tablename__ = 'shows'

  id = db.Column(db.Integer, primary_key=True)
  start_time = db.Column(db.DateTime)
  venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
  artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)

#Area
class Area(db.Model):
  __tablename__ = 'area'

  id = db.Column(db.Integer, primary_key=True)
  city = db.Column(db.String)
  state = db.Column(db.String)
  venue = db.relationship('Venue', backref=db.backref('area', lazy=True))
