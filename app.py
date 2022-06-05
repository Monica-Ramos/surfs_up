
#import dependencies
import datetime as dt
import numpy as np
import pandas as pd

#import dependecies for SQLAlchemy
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#set up the database, allows us to access and query our SQLite database file
engine = create_engine("sqlite:///hawaii.sqlite")

#reflect our databse into classes
Base = automap_base()
#Reflect databse
Base.prepare(engine, reflect=True)

#create a variable for each classes
Measurement = Base.classes.measurement
Station = Base.classes.station

#Finally, create a session link from Python to our database with the following code:

session = Session(engine)

#SET UP FLASK
#create a new flask instance
app = Flask(__name__)

#create flask route
@app.route('/')

#create a function called welcome()
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

#create a function called hello_world()
#@app.route('/')
#def hello_world():
    #return 'Hello world'


#create precipitation route
@app.route("/api/v1.0/precipitation")

#create precipitation function

def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_year).all()
    #create a dictionary with the date as the key and the precipitation as the value
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)


#create stations route
@app.route("/api/v1.0/stations")

#create stations function
def stations():
    results = session.query(Station.station).all()
    #uravel results into one dimensional array(list)
    stations = list(np.ravel(results))
    #jsonify the list and return it as JSON
    return jsonify(stations=stations)

#create monthly temp route
@app.route("/api/v1.0/tobs")

#create function called monthly_temp
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)


#Create Statistics Route
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

#create a function
def stats(start=None, end=None):
    #select min, avg and max temp
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        #the asterisk is used to indicate there will be multiple results for our query: minimum, average, and maximum temperatures.
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)
