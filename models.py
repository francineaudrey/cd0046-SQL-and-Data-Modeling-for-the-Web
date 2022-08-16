from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import ForeignKey
from flask_moment import Moment
from flask import Flask
from flask_migrate import Migrate

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

    
class Venue(db.Model):
    __tablename__ = 'venue'
    __table_args__ = (db.UniqueConstraint('name', 'city', 'address','state','phone',name='unique_constraint_name_city_address_state_phone'),)
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(120)), nullable=False)
    facebook_link = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    website_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean,default=False)
    seeking_description = db.Column(db.String(10000))
    show = db.relationship('show', backref=db.backref('venue', lazy=True))
    def __repr__(self):
        return f'<city: {self.city}, state: {self.state}>'


class Artist(db.Model):
    __tablename__ = 'artist'
    __table_args__ = (db.UniqueConstraint('name','city','state','phone',name='unique_constraint_name_city_state_phone'),)
    

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(120)), nullable=False)
    facebook_link = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    website_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean,default=False)
    seeking_description = db.Column(db.String(10000))  
    show = db.relationship('show', backref=db.backref('artist', lazy=True))

class Show(db.Model):
    __tablename__ = 'show'

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, ForeignKey('artist.id'), nullable=False)
    venue_id = db.Column(db.Integer, ForeignKey('venue.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    def __repr__(self):
      return f'<date: {self.start_time}, venue_id: {self.venue_id}, artist_id: {self.artist_id}>'



#db.create_all()


