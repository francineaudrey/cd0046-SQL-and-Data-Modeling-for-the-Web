#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from copy import error
import json
from operator import and_
from unicodedata import name
import dateutil.parser
import babel
from models import Show, Venue, Artist
from flask_migrate import Migrate
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from markupsafe import Markup
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# TODO: connect to a local postgresql database

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:0000@localhost:5432/fyyur_database"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#



    # TODO: implement any missing fields, as a database migration using Flask-Migrate
         

   
    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

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
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.

  city_state = db.session.query(Venue.city, Venue.state).group_by(Venue.city, Venue.state).all()

  data = []

  for city in city_state:
        city = dict(city)
        venues = db.session.query(Venue.id,Venue.name,).filter(and_(Venue.city == city.city,Venue.state == city.state)).all()
        city['venues'] = [{
            'id': venue.id,
            'name': venue.name,
            'num_upcoming_shows': Show.query.filter(Show.venue_id == venue.id).count()
        } for venue in venues]
        data.append(city)

  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

  search_term = request.form['search_term']
  response = {}
  response['data'] = []
  formatted_input = '%{0}%'.format(search_term)
  venues = Venue.query.filter(Venue.name.ilike(formatted_input)).all()
  for venue in venues:
    data = {}
    data['id'] = venue.id
    data['name'] = venue.name
    response['data'].append(data)
  response['count'] = len(response['data'])

  db.session.close()
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
        # TODO: replace with real venue data from the venues table, using venue_id
    venue=Venue.query.get(venue_id)
    
    upcoming_shows = []
    upcoming = db.session.query(Show).join(Artist).filter(Show.venue_id == venue_id).filter(Show.start_time > datetime.now()).all()

    for show in upcoming:
        upcoming_shows.append({
            'artist_id': show.artist_id,
            'artist_name': show.artists.name,
            'artist_image_link': show.artists.image_link,
            'start_time': show.start_time
        })

    past_shows = []
    past = db.session.query(Show).join(Artist).filter(Show.venue_id == venue_id).filter(Show.start_time < datetime.now()).all()

    for show in past:
        upcoming_shows.append({
            'artist_id': show.artist_id,
            'artist_name': show.artists.name,
            'artist_image_link': show.artists.image_link,
            'start_time': show.start_time
        })

    data = {
        'id': venue.id,
        'name': venue.name,
        'genres': venue.genres,
        'address': venue.address,
        'city': venue.city,
        'state': venue.state,
        'phone': venue.phone,
        'image_link': venue.image_link,
        'facebook_link': venue.facebook_link,
        'website_link': venue.website_link,
        'seeking_talent': True,
        'seeking_description': venue.seeking_description,
        'past_shows': past_shows,
        'upcoming_shows': upcoming_shows,
        'past_shows_number': len(past_shows),
        'upcoming_shows_number': len(upcoming_shows),
    }

    print(upcoming_shows, past_shows)

    data1 = list(filter(lambda d: d['id'] == venue_id, data))[0]

    return render_template('pages/show_venue.html', venue=data1)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET', 'POST'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
   error = False
   try:
    form = VenueForm(request.form)
    if form.validate():
         name = form.name.data
         city = form.city.data
         state = form.state.data
         address = form.address.data
         phone = form.phone.data
         genres = form.genres.data
         facebook_link = form.facebook_link.data
         image_link = form.image_link.data
         website_link = form.website_link.data
         seeking_talent = form.seeking_talent.data
         seeking_description = form.seeking_description.data

         venue = Venue(name=name,city=city,state=state,
         address=address,phone=phone,genres=genres,
         facebook_link=facebook_link,image_link=image_link,
         website_link=website_link,seeking_talent=seeking_talent,
         seeking_description=seeking_description)    
         db.session.add(venue)
         db.session.commit()
    else:
      error = True
   except:
    error = True
   finally:
    db.session.close()

   if error:
      flash('An error occurred. Venue ' + request.form['name'] 
            + ' could not be listed.')
   else:
         flash('venue ' + request.form['name'] + ' was successfully listed!')

   return redirect('pages/home.html')

    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion

    # on successful db insert, flash success
    #flash('Venue ' + request.form['name'] + ' was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    #return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
 try:
   venue=Venue.query.get(venue_id)
   db.session.delete(venue)
   db.session.commit
 except:
   db.session.rollback()
 finally:
   db.session.close()

 return None
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
 

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  artists=Artist.query.get.all
  return render_template('pages/artists.html', artists)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term = request.form['search_term']
  response={}
  response['data'] = []
  formatted_input = '%{0}%'.format(search_term)
  artists = Artist.query.filter(Venue.name.ilike(formatted_input)).all()
  for artist in artists:
    data = {}
    data['id'] = artist.id
    data['name'] = artist.name
    response['data'].append(data)
  response['count'] = len(response['data'])

  db.session.close()
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  artist_list=Artist.query.get(artist_id)
  data = []
  for artist in artist_list:
      artist_data = {}
      artist_data['id'] = artist.id
      artist_data['name'] = artist.name
      data.append(artist_data)
  db.session.close()
  data = list(filter(lambda d: d['id'] == artist_id, [artist]))[0]
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.get(artist_id)
  artist1={}
  artist1['id'] = artist.id
  artist1['name'] = artist.name
  artist1['genres'] = artist.genres
  artist1['city'] = artist.city
  artist1['state'] = artist.state
  artist1['phone'] = artist.phone
  artist1['website'] = artist.website
  artist1['facebook_link'] = artist.facebook_link
  artist1['seeking_venue'] = artist.seeking_venue
  artist1['seeking_description'] = artist.seeking_description
  artist1['image_link'] = artist.image_link

  form.name.data = artist1['name']
  form.city.data = artist1['city']
  form.state.data = artist1['state']
  form.phone.data = artist1['phone']
  form.genres.data = artist1['genres']
  form.facebook_link.data = artist1['facebook_link']
  form.image_link.data = artist1['image_link']
  form.website_link.data = artist1['website']
  form.seeking_venue.data = artist1['seeking_venue']
  form.seeking_description.data = artist1['seeking_description']
  db.session.close()
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist1)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  form = ArtistForm()
  if form.validate():
    name = form.name.data
    city = form.city.data
    state = form.state.data
    phone = form.phone.data
    genres = form.genres.data
    facebook_link = form.facebook_link.data
    image_link = form.image_link.data
    website_link = form.website_link.data
    seeking_venue = form.seeking_description.data
    seeking_description = form.seeking_description.data

    artist = Artist.query.get(artist_id)
    artist.name = name
    artist.city = city
    artist.state = state
    artist.phone = phone
    artist.genres = genres
    artist.facebook_link = facebook_link
    artist.image_link = image_link
    artist.website_link = website_link
    artist.seeking_venue = seeking_venue
    artist.seeking_description = seeking_description
  else:
    flash('Oops, sorry there is an error!')

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venues={}
  venue = Venue.query.get(venue_id)
  venues['id'] = venue.id
  venues['name'] = venue.name
  venues['genres'] = venue.genres
  venues['state'] = venue.state
  venues['city'] = venue.city
  venues['phone'] = venue.phone
  venues['address'] = venue.address
  venues['facebook_link'] = venue.facebook_link
  venues['image_link'] = venue.image_link
  venues['website_link'] = venue.website_link
  venues['seeking_talent'] = venue.seeking_talent
  venues['seeking_description'] = venue.seeking_description

  form.name.data = venues['name']
  form.address.data = venues['address']
  form.city.data = venues['city']
  form.state.data = venues['state']
  form.genres.data = venues['genres']
  form.facebook_link.data = venues['facebook_link']
  form.image_link.data = venues['image_link']
  form.website_link.data = venues['image_link']
  form.seeking_talent.data = venues['seeking_talent']
  form.seeking_description = venues['seeking_description']
  db.session.close()

      # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
    
  error= False
  venue_modif=Venue.query.get(venue_id)

  try:
    name=request.form.data('name')
    city = request.form.data('city')
    state = request.form.data('state')
    phone = request.form.data('phone')
    address=request.form.data('address')
    image_link = request.form.data('image_link')
    facebook_link = request.form.data('facebook_link')
    genres = request.form.datalist('genres')
    website_link = request.form.data('website_link')
    seeking_talent = request.form.data('seeking_talent')
    seeking_description  = request.form.data('seeking_description')

    venue_modif.name=name
    venue_modif.city=city
    venue_modif.state=state
    venue_modif.phone=phone
    venue_modif.address=address
    venue_modif.genres=genres
    venue_modif.image_link=image_link
    venue_modif.facebook_link=facebook_link
    venue_modif.website_link=website_link
    venue_modif.seeking_talent=seeking_talent
    venue_modif.seeking_description=seeking_description
    db.session.commit()
  except TypeError:
    db.session.rollbacK()
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
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  error = False
  try:
    form = VenueForm()
    if form.validate_on_submit():
         name = form.name.data
         city = form.city.data
         state = form.state.data
         address = form.address.data
         phone = form.phone.data
         genres = form.genres.data
         facebook_link = form.facebook_link.data
         image_link = form.image_link.data
         website_link = form.website_link.data
         seeking_talent = form.seeking_talent.data
         seeking_description = form.seeking_description.data

         venue = Venue(name=name,city=city,state=state,address=address,phone=phone,genres=genres,facebook_link=facebook_link,image_link=image_link,website_link=website_link,seeking_talent=seeking_talent,seeking_description=seeking_description)    
         db.session.add(venue)
         db.session.commit()
    else:
      error = True
  except:
    error = True
  finally:
    db.session.close()

  if error:
      flash('An error occurred. Artist ' + ['name'] + ' could not be listed.')
  else:
      flash('Artist ' + request.form['name'] + ' was successfully listed!')

  return render_template('pages/home.html')

  # on successful db insert, flash success
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., 


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows

  # TODO: replace with real venues data.
  data=[]
  shows_list=db.session.query(Show).join(Venue,Venue.id == Show.venue_id).join(Artist, Artist.id == Show.artist_id).all()
  for show in shows_list:
    reference_show={
      'venue_id':show.venue_id,
      'venue_name':show.venue.name,
      'artist_id':show.artist_id,
      'artist_name':show.artist.name,
      'artist_image_link':show.artist.image_link,
      'start_time':show.start_time
    }
    data.append(reference_show)
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  error = False
  try:
    form = ShowForm(request.form)
    if form.validate():
      artist_id =form.artist_id.data
      venue_id =form.venue_id.data
      date =form.start_time.data
      data = Show(artist_id=artist_id, venue_id=venue_id, date=date)
      db.session.add(data)
      db.session.commit()
    else:
      error = True
  except:
    error = True
  finally:
    db.session.close()

  if error:
    flash('An error occurred. Show could not be listed.')
  else:
    flash('Show was successfully listed!')
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

if __name__ == '__main__':
    port = int(('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

