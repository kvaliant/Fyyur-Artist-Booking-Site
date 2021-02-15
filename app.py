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

# Import model from models.py
from models import Artist, Venue, Area, Shows

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
  # TODO DONE: insert form data as a new Venue record in the db, instead
  # TODO DONE: modify data to be the data object returned from db insertion

  name = request.form['name']
  city = request.form['city']
  state = request.form['state']
  address = request.form['address']
  phone = request.form['phone']
  try:
    if(request.form['seeking_talent'] == 'y'):
      seeking_talent = True
  except:
    seeking_talent = False
  seeking_description = request.form['seeking_description']
  genres = request.form.getlist('genres')
  image_link = request.form['image_link']
  website = request.form['website']
  facebook_link = request.form['facebook_link']
  error = False
  try:
      venue = Venue(name=name, city=city, state=state, address=address, phone=phone, seeking_talent=seeking_talent, seeking_description=seeking_description, genres=genres, facebook_link=facebook_link, website=website, image_link=image_link)
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
  # TODO DONE: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  venue = Venue.query.filter_by(id=venue_id).first()
  if(Venue.query.filter_by(id=venue_id).count() == 1):
    name = venue.name
  error = False
  try:
    #delete shows related to this venue
    shows = Shows.query.filter_by(venue_id=venue_id).all()
    for show in shows:
      db.session.delete(show)
    #delete this venue's area if area only contain this venue
    area = Area.query.filter_by(id = venue.area_id).first()
    if(Venue.query.filter_by(area_id=area.id).count() == 1):
      db.session.delete(area)
    db.session.delete(venue)
    db.session.commit()
  except:
    db.session.rollback()
    error = True
  finally:
    db.session.close()    
  if error:
    # TODO DONE: on unsuccessful db insert, flash an error instead.
    flash('An error occurred.')
  else:
    # on successful db insert, flash success
    flash('Venue ' + name + ' was successfully deleted!')

  return render_template('pages/home.html')

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
  artist=Artist.query.filter_by(id=artist_id).first()
  # TODO DONE: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO DONE: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  name = request.form['name']
  city = request.form['city']
  state = request.form['state']
  phone = request.form['phone']
  try:
    if(request.form['seeking_venue'] == 'y'):
      seeking_venue = True
  except:
    seeking_venue = False
  seeking_description = request.form['seeking_description']
  genres = request.form.getlist('genres')
  image_link = request.form['image_link']
  facebook_link = request.form['facebook_link']
  website = request.form['website']
  error = False
  try:
      artist = Artist.query.filter_by(id=artist_id).first()
      artist.name = name
      artist.city = city
      artist.state = state
      artist.phone = phone
      artist.seeking_venue = seeking_venue
      artist.seeking_description = seeking_description
      artist.genres = genres
      artist.image_link = image_link
      artist.facebook_link = facebook_link
      artist.website = website
      db.session.commit()
  except:
      db.session.rollback()
      error = True
  finally:
      db.session.close()    
  if error:
      # on unsuccessful db insert, flash an error instead.
      flash('An error occurred.')
  else:
      # on successful db insert, flash success
      flash('Artist ' + name + ' was successfully edited!')

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.filter_by(id=venue_id).first()
  # TODO DONE: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO DONE: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes

  name = request.form['name']
  city = request.form['city']
  state = request.form['state']
  address = request.form['address']
  phone = request.form['phone']
  try:
    if(request.form['seeking_talent'] == 'y'):
      seeking_talent = True
  except:
    seeking_talent = False
  seeking_description = request.form['seeking_description']
  genres = request.form.getlist('genres')
  image_link = request.form['image_link']
  website = request.form['website']
  facebook_link = request.form['facebook_link']
  error = False
  try:
    venue = Venue.query.filter_by(id=venue_id).first()
    # if city/ state (area) changed
    if(venue.city != city):
      # Declare previous area for delete later
      prev_area = Area.query.filter_by(id = venue.area_id).first()
      # What todo with new area
      if(Area.query.filter_by(city=city, state=state).count() == 1):
        #if area exist
        area_id = Area.query.filter_by(city=city, state=state).first().id
        venue.area_id = area_id
      else:
        area = Area(city= city, state= state)   
        db.session.add(area)
        area_id = Area.query.filter_by(city=city, state=state).first().id        
        venue.area_id = area_id
      # Only delete prev_area after changes
      if(Venue.query.filter_by(area_id=prev_area.id).count() == 0):
        db.session.delete(prev_area)
    venue.name = name
    venue.city = city
    venue.state = state
    venue.phone = phone
    venue.seeking_talent = seeking_talent
    venue.seeking_description = seeking_description
    venue.genres = genres
    venue.image_link = image_link
    venue.facebook_link = facebook_link
    venue.website = website
    db.session.commit()
  except:
    db.session.rollback()
    error = True
  finally:
    db.session.close()    
  if error:
    # on unsuccessful db insert, flash an error instead.
    flash('An error occurred.')
  else:
    # on successful db insert, flash success
    flash('Venue ' + name + ' was successfully edited!')


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
  try:
    if(request.form['seeking_venue'] == 'y'):
      seeking_venue = True
  except:
    seeking_venue = False
  seeking_description = request.form['seeking_description']
  genres = request.form.getlist('genres')
  image_link = request.form['image_link']
  facebook_link = request.form['facebook_link']
  website = request.form['website']
  error = False
  try:
      artist = Artist(name=name, city=city, state=state, phone=phone, seeking_venue=seeking_venue, seeking_description=seeking_description, genres=genres, facebook_link=facebook_link, website=website, , image_link=image_link)
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
  # TODO DONE: replace with real venues data.
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
