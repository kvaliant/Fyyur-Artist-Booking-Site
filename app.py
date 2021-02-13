#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *

# ADDITIONAL DONE: additional Imports
from flask_migrate import Migrate

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# TODO DONE: connect to a local postgresql database

# ADDITIONAL DONE: migration
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

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

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO DONE: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data= Area.query.all()
  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO DONE: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term=request.form.get('search_term','')
  response= {
    "count": Venue.query.filter(Venue.name.ilike('%'+search_term+'%')).count(),
    "data": Venue.query.filter(Venue.name.ilike('%'+search_term+'%')).all()
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO DONE: replace with real venue data from the venues table, using venue_id
  venue = Venue.query.filter_by(id=venue_id).first()
  current_time = datetime.utcnow()
  past_shows = Shows.query.filter(Shows.venue_id==venue_id, Shows.start_time < current_time).all()
  past_shows_count = Shows.query.filter(Shows.venue_id==venue_id, Shows.start_time < current_time).count()
  upcoming_shows = Shows.query.filter(Shows.venue_id==venue_id, Shows.start_time > current_time).all()
  upcoming_shows_count = Shows.query.filter(Shows.venue_id==venue_id, Shows.start_time > current_time).count()
  data= {
    "id": venue.id,
    "name": venue.name,
    "genres": venue.genres,
    "city": venue.city,
    "state": venue.state,
    "address": venue.address,
    "phone": venue.phone,
    "website": venue.website,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "image_link": venue.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": past_shows_count,
    "upcoming_shows_count": upcoming_shows_count,
  }
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  name = request.form['name']
  city = request.form['city']
  state = request.form['state']
  address = request.form['address']
  phone = request.form['phone']
  genres = request.form.getlist('genres')
  facebook_link = request.form['facebook_link']
  error = False
  try:
      venue = Venue(name=name, city=city, state=state, address=address, phone=phone, genres=genres, facebook_link=facebook_link)
      if(Area.query.filter_by(city=city, state=state).count() == 1):
        #if area exist
        area_id = Area.query.filter_by(city=city, state=state).first().id
        venue.area_id = area_id
      else:
        area = Area(city= city, state= state)   
        area.venue = [venue]
        db.session.add(area)
      db.session.add(venue)
      db.session.commit()
  except:
      db.session.rollback()
      error = True
  finally:
      db.session.close()    
  if error:
      # TODO DONE: on unsuccessful db insert, flash an error instead.
      flash('An error occurred. Venue ' + name + ' could not be listed.')
  else:
      # on successful db insert, flash success
      flash('Venue ' + name + ' was successfully listed!')

  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO DONE: replace with real data returned from querying the database
  data= Artist.query.all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO DONE: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term=request.form.get('search_term','')
  response= {
    "count": Artist.query.filter(Artist.name.ilike('%'+search_term+'%')).count(),
    "data": Artist.query.filter(Artist.name.ilike('%'+search_term+'%')).all()
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO DONE: replace with real venue data from the venues table, using venue_id
  artist = Artist.query.filter_by(id=artist_id).first()
  current_time = datetime.utcnow()
  past_shows = Shows.query.filter(Shows.artist_id==artist_id, Shows.start_time < current_time).all()
  past_shows_count = Shows.query.filter(Shows.artist_id==artist_id, Shows.start_time < current_time).count()
  upcoming_shows = Shows.query.filter(Shows.artist_id==artist_id, Shows.start_time > current_time).all()
  upcoming_shows_count = Shows.query.filter(Shows.artist_id==artist_id, Shows.start_time > current_time).count()
  data= {
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": past_shows_count,
    "upcoming_shows_count": upcoming_shows_count,
  }
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist={
    "id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO DONE: insert form data as a new Venue record in the db, instead
  # TODO DONE: modify data to be the data object returned from db insertion

  name = request.form['name']
  city = request.form['city']
  state = request.form['state']
  phone = request.form['phone']
  genres = request.form.getlist('genres')
  facebook_link = request.form['facebook_link']
  error = False
  try:
      artist = Artist(name=name, city=city, state=state, phone=phone, genres=genres, facebook_link=facebook_link)
      db.session.add(artist)
      db.session.commit()
  except:
      db.session.rollback()
      error = True
  finally:
      db.session.close()    
  if error:
      # TODO DONE: on unsuccessful db insert, flash an error instead.
      flash('An error occurred. Artist ' + name + ' could not be listed.')
  else:
      # on successful db insert, flash success
      flash('Artist ' + name + ' was successfully listed!')

  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data=Shows.query\
  .join(Artist, Shows.artist_id==Artist.id)\
  .join(Venue, Shows.venue_id==Venue.id)\
  .add_columns(Shows.start_time, Shows.artist_id, Shows.venue_id, Artist.name.label("artist_name"), Venue.name.label("venue_name"), Venue.image_link.label("venue_image_link")).all()
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO DONE: insert form data as a new Show record in the db, instead  

  artist_id = request.form['artist_id']
  venue_id = request.form['venue_id']
  start_time = request.form['start_time']
  if(Artist.query.filter_by(id=artist_id).count() == 1 & Venue.query.filter_by(id=venue_id).count() == 1):
    error = False
    try:
        show = Shows(artist_id = artist_id, venue_id = venue_id, start_time = start_time)
        db.session.add(show)
        db.session.commit()
    except:
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()    
    if error:
        abort (400)
        flash('An error occurred. Show could not be listed.')
    else:
        # on successful db insert, flash success
        flash('Show was successfully listed!')
  else:
    flash('An error occurred. Show could not be listed. invalid')

  # TODO DONE: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
