#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
from flask_migrate import Migrate
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for,jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
import sys
from flask_wtf.csrf import CsrfProtect
from sqlalchemy.orm import sessionmaker
from operator import itemgetter 

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
# connection to postgresql database
app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app,db)


# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
# Creating Venue Model
class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    Venue_name = db.Column(db.String,nullable = False)
    city = db.Column(db.String(120),nullable = False)
    state = db.Column(db.String(120),nullable = False)
    genres = db.Column(db.ARRAY(db.String))
    address = db.Column(db.String(120),nullable = False)
    phone = db.Column(db.String(120),nullable = False)
    image_link = db.Column(db.String(500),nullable = True)
    facebook_link = db.Column(db.String(120),nullable = True)
    seeking_talent = db.Column(db.Boolean,nullable = True,default = False)
    seeking_description = db.Column(db.String(120),nullable = True,default='')
    website = db.Column(db.String(500),nullable = True)
    show = db.relationship('Show',backref = 'venue',lazy ='dynamic')

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# Creating Artist Model
class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String,nullable = False)
    city = db.Column(db.String(120),nullable = False)
    state = db.Column(db.String(120),nullable = False)
    phone = db.Column(db.String(120),nullable = False)
    genres = db.Column(db.ARRAY(db.String))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean,nullable = False,default = False)
    seeking_description = db.Column(db.String(120),nullable = True,default='')
    website = db.Column(db.String(500),nullable = True)
    show = db.relationship('Show',backref = 'artist',lazy ='dynamic')

  # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

# Creating Venue Model
class Show(db.Model):
  __tablename__ = 'Show'
  id = db.Column(db.Integer,primary_key = True)
  start_time = db.Column(db.String(),nullable = False)
  artist_id= db.Column(db.Integer, db.ForeignKey('Artist.id'),nullable=False)
  venue_id = db.Column(db.Integer,db.ForeignKey('Venue.id'),nullable = False)
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
  # TODO: replace with real venues data.
  # num_shows should be aggregated based on number of upcoming shows per venue.
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    result = Venue.query.group_by(Venue.id, Venue.state, Venue.city).all()

    city_and_state = ''

    data = []

    for venue in result:

        upcoming_shows = venue.show.filter(Show.start_time > current_time).all()
        if city_and_state == venue.city + venue.state:
            data[len(data) - 1]["venues"].append({
              "id": venue.id,
              "name": venue.Venue_name,
              "num_upcoming_shows": len(upcoming_shows)
            })

        else:
            city_and_state = venue.city + venue.state
            data.append({
              "city": venue.city,
              "state": venue.state,
              "venues": [{
                "id": venue.id,
                "name": venue.Venue_name,
                "num_upcoming_shows": len(upcoming_shows)
              }]
            })

    return render_template('pages/venues.html', areas=data)
########################################################################################
@app.route('/venues/search', methods=['POST','GET'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term=request.form.get('search_term').lower()

  result1 = Venue.query.add_columns(Venue.id , Venue.Venue_name).all()

  result2 = Show.query.join(Venue, Venue.id == Show.venue_id ).count()

  count = 0

  #initial valuses for respone in case there is a match
  for i in result1:

    if (search_term not in i.Venue_name.lower()):
      response={
      "count": 0,"data": [{
      "id":None,"name":None
      ,"num_upcoming_shows":None}]
      }

    else:
      count = count+1
      response={
    "count": count,
    "data": [{
      "id": i[0].id,
      "name": i[0].Venue_name,
      "num_upcoming_shows": result2,
    }]
  }  
      break
  for i in result1:
    if (search_term in i.Venue_name.lower() ) :
      count = count+1
      response['data'].append({"id":i.id,"name":i.Venue_name,"num_upcoming_shows":result2})
      response['count']=count

  #deleting the first record so we avoid having duplacte search results
  if(count >= len(response)):
    response['data'].pop(0)
    response['count'] = count - 1  

  if (response['count'] == 0):
    flash('Sorry this artist does not exist!')


  return render_template('pages/search_venues.html', results=response, search_term=search_term)
########################################################################################
@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  result = Venue.query.get(venue_id)

  show_result = Show.query.join(Artist).filter(Show.venue_id == venue_id).all()

  artist_result = Artist.query.join(Show).filter(Show.artist_id == Artist.id ).filter(Show.venue_id == venue_id).all()

  current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


  
  data1={
    "id": result.id,
    "name": result.Venue_name,
    "genres": result.genres,
    "address": result.address,
    "city": result.city,
    "state": result.state,
    "phone": result.phone,
    "website": result.website,
    "facebook_link": result.facebook_link,
    "seeking_talent": result.seeking_talent,
    "seeking_description": result.seeking_description,
    "image_link": result.image_link,
    "past_shows": [],
    "upcoming_shows": [],
    "past_shows_count": 0,
    "upcoming_shows_count": 0,
  }

  past_count = 0
  upcoming_count=0
  count = 0

  #arranging the order of shows per venue 
  for artist in artist_result :

    time = show_result[count]
    if (current_time > str(time.start_time)):

      data1['past_shows'].append({"artist_id": artist.id,
      "artist_name": artist.name,
      "artist_image_link": artist.image_link,
      "start_time": str(time.start_time)})
      data1['past_shows_count']= past_count =past_count+1
      count = count+1

    else:

       data1['upcoming_shows'].append({"artist_id": artist.id,
      "artist_name": artist.name,
      "artist_image_link": artist.image_link,
      "start_time": str(time.start_time)})
       data1['upcoming_shows_count']= upcoming_count =upcoming_count+1
       count =count+1
        
  data = list(filter(lambda d: d['id'] == venue_id, [data1]))[0]

  return render_template('pages/show_venue.html', venue=data)
########################################################################################
#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)
########################################################################################
@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  form = VenueForm()

  #checking if form submission is valid and then creating a venue record
  if not form.validate():
    flash( form.errors )
    return redirect(url_for('create_venue_form'))
  error = False
  try:
    name = request.form['name']
    city = request.form['city']
    state = request.form['state']
    address = request.form['address']
    phone = request.form['phone']
    genres = request.form.getlist('genres')
    facebook_link = request.form['facebook_link']
    image_link = request.form['image_link']
    newVenue = Venue(Venue_name = name , city = city , state = state , address = address ,
    phone = phone , genres = genres , facebook_link = facebook_link,image_link=image_link) 
    db.session.add(newVenue)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    if error:
      flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
    else:
      flash('Venue ' + request.form['name'] + ' was successfully listed!')
    db.session.close()  

  # TODO: on unsuccessful db insert, flash an error instead.
  #see: http://flask.pocoo.org/docs/1.0/patterns/flashing/

  return render_template('pages/home.html')

########################################################################################
@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  #Note : on delete reload the page in order to see the new venue list
  try:
   deleted_venue = Venue.query.filter_by(id = venue_id).one()
   db.session.delete(deleted_venue)
   db.session.commit()
  except:
    flash('Venue Can not be deleted try again!') 
    db.session.rollback()
  finally:
    db.session.close() 

  # for some reason i couldn't make the page reload by its self

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return json.dumps({'success':True}), 200, {'ContentType':'application/json'} , redirect(url_for('index'))

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  result = Artist.query.all()

  data = []

  for i in result:
    data.append(i)
   
   
  return render_template('pages/artists.html', artists=data)
########################################################################################
@app.route('/artists/search', methods=['POST','GET'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  result = Artist.query.add_columns(Artist.name , Artist.id).all()

  result2 = Show.query.join(Artist, Artist.id==Show.artist_id ).count()

  count = 0

  search_term =request.form.get('search_term').lower()

  #initial valuses for respone in case there is a match
  for i in result:

    if (search_term not in i.name.lower()):
      response={
      "count": 0,"data": [{
      "id":None,"name":None
      ,"num_upcoming_shows":None}]
      }

    else:
      count = count+1
      response={
    "count": count,
    "data": [{
      "id": i[0].id,
      "name": i[0].name,
      "num_upcoming_shows": result2,
    }]
  }  
      break
  for i in result:
    if (search_term in i.name.lower() ) :
      count = count+1
      response['data'].append({"id":i.id,"name":i.name,"num_upcoming_shows":result2})
      response['count']=count

  #deleting the first record so we avoid having duplacte search results
  if(count >= len(response)):
    response['data'].pop(0)
    response['count'] = count - 1  

  if (response['count'] == 0):
    flash('Sorry this artist does not exist!')

  return render_template('pages/search_artists.html', results=response,search_term=search_term)

########################################################################################
@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  result = Artist.query.get(artist_id)
  venue_result = Venue.query.join(Show).filter(Show.artist_id == artist_id).all()
  show_result = Show.query.join(Venue).filter(Show.artist_id == artist_id).all()
  current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

  data1={
    "id": result.id,
    "name": result.name,
    "genres":result.genres,
    "city": result.name,
    "state": result.state,
    "phone": result.phone,
    "website": result.website,
    "facebook_link": result.facebook_link,
    "seeking_talent": result.seeking_talent,
    "seeking_description": result.seeking_description,
    "image_link": result.image_link,
    "past_shows": [],
    "upcoming_shows": [],
    "past_shows_count": 0,
    "upcoming_shows_count": 0,
  }
  past_count = 0
  upcoming_count = 0
  count = 0

  #arranging order of shows per venue
  for venue in venue_result:

    time = show_result[count]
    if (current_time > str(time.start_time)):
      data1['past_shows'].append({"venue_id": venue.id,
      "venue_name": venue.Venue_name,
      "venue_image_link": venue.image_link,
      "start_time": str(time.start_time)})
      data1['past_shows_count']= past_count = past_count+1
      count = count+1

    else:   
       data1['upcoming_shows'].append({"venue_id": venue.id,
      "venue_name": venue.Venue_name,
      "venue_image_link": venue.image_link,
      "start_time": str(time.start_time)})
       data1['upcoming_shows_count']  = upcoming_count= upcoming_count+1
       count = count+1


  data = list(filter(lambda d: d['id'] == artist_id, [data1]))[0]

  return render_template('pages/show_artist.html', artist=data)
########################################################################################
#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  #editing uses another artist form 
  form = ArtistForm2()

  result = Artist.query.get(artist_id)

  artist = Artist(name = result.name,id = result.id,city = result.city,
  phone = result.phone,genres = result.genres,facebook_link = result.facebook_link
  ,image_link = result.image_link)

  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  result = Artist.query.get(artist_id)
  error = False

  try:
    result.name = request.form['name']
    result.city = request.form['city']
    result.state = request.form['state']
    result.phone = request.form['phone']
    result.genres = request.form.getlist('genres')
    result.facebook_link = request.form['facebook_link']
    result.website = request.form['website']
    result.seeking_description = request.form['seeking_description']
    result.seeking_talent = request.form.get('seeking_talent')
    result.image_link = request.form['image_link']

    #checking the seeking_talent value where 'y' is true and 'n' is false
    if (result.seeking_talent == 'y'):
      result.seeking_talent = True
    else:
      result.seeking_talent = False  

    db.session.commit() 
  except:
     error = True
     db.session.rollback()
  finally:
    if error:
      flash('Opss!,An error occurred. Artist ' + request.form['name'] + ' could not be updated.')
    else:    
      flash('Artist ' + request.form['name'] + ' was successfully updted!')
    db.session.close()             


  return redirect(url_for('show_artist', artist_id=artist_id))
########################################################################################
@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  #editing uses another venue form 
  form = VenueForm2()

  result = Venue.query.get(venue_id)

  venue = Venue(Venue_name = result.Venue_name,id = result.id,city = result.city,
  state = result.state,address = result.address , phone = result.phone,image_link = result.image_link,
  facebook_link =result.facebook_link)


  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)
########################################################################################
@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  result = Venue.query.get(venue_id)
  error = False
  try:
   
    result.Venue_name = request.form['name']
    result.city = request.form['city']
    result.state = request.form['state']
    result.address = request.form['address']
    result.phone = request.form['phone']
    result.genres = request.form.getlist('genres')
    result.facebook_link = request.form['facebook_link']
    result.website = request.form['website']
    result.seeking_description = request.form['seeking_description']
    result.seeking_talent = request.form.get('seeking_talent')
    result.image_link = request.form['image_link']

    #checking the seeking_talent value where 'y' is true and 'n' is false
    if (result.seeking_talent == 'y'):
      result.seeking_talent = True
    else:
      result.seeking_talent = False  
      
    db.session.commit()
  except:
    error = True
    db.session.rollback()
  finally:
    if error:
      flash('An error occurred. Venue ' + request.form['name'] + ' could not be updated.')
    else:
      flash('Venue ' + request.form['name'] + ' was successfully updted!')
    db.session.close() 


  return redirect(url_for('show_venue', venue_id=venue_id))
########################################################################################
#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)
########################################################################################
@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  form = ArtistForm()

  #checking if the form is valid 
  if not form.validate():
    flash( form.errors )
    return redirect(url_for('create_artist_form'))

  error = False
  try:
    name = request.form['name']
    city = request.form['city']
    state = request.form['state']
    phone = request.form['phone']
    genres = request.form.getlist('genres')
    facebook_link = request.form['facebook_link']
    image_link = request.form['image_link']
    newArtist = Artist(name = name ,city = city,state=state,phone = phone,
    genres = genres ,facebook_link = facebook_link,image_link = image_link)
    db.session.add(newArtist)
    db.session.commit()
  except:
   error = True 
   db.session.rollback()
  finally:
    if error:
      flash('Opss!,An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
    else:    
      flash('Artist ' + request.form['name'] + ' was successfully listed!')
      
    db.session.close()

  # TODO: on unsuccessful db insert, flash an error instead.
  return render_template('pages/home.html')
########################################################################################

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  # num_shows should be aggregated based on number of upcoming shows per venue.
  
  result = Show.query.join(Venue ,Venue.id == Show.venue_id).join(Artist
  ,Artist.id == Show.artist_id ).add_columns(Venue.id ,Venue.Venue_name,
  Show.start_time,Show.artist_id,Show.venue_id,Artist.name,Artist.image_link).all()

  data = []
  for i in result:
    data.extend([{ "venue_id": i.venue_id,
    "venue_name": i.Venue_name,
    "artist_id": i.artist_id,
    "artist_name": i.name,
    "artist_image_link": i.image_link,
    "start_time": str(i.start_time),
    "Num_shows": i.start_time
  }])
   
  return render_template('pages/shows.html', shows=data)
########################################################################################
@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)
########################################################################################
@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  error = False
  try:
    artist_id = request.form['artist_id']
    venue_id = request.form['venue_id']
    start_time = request.form['start_time']
    newShow = Show(artist_id = artist_id , venue_id = venue_id ,
    start_time = start_time)
    db.session.add(newShow)
    db.session.commit()

  except:
    error = True
    db.session.rollback()
    print(sys.exc_info)

  finally:
    if error:
      flash('An error occurred. Show could not be listed.')   
    else:
      flash('Show was successfully listed!')

  db.session.close()  

  return render_template('pages/home.html')
########################################################################################
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404
########################################################################################
@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500
########################################################################################

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
#WORK BY : ANASS MARKHOUSS 