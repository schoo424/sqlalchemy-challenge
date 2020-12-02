import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    print ("""List all available api routes.""")
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start> and /api/v1.0/<start>/<end>"
    )

# Precipitation route
@app.route("/api/v1.0/precipitation")
def precips():
    # Start the session for the page
    session = Session(engine)

    precip = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > '2016-08-22').all()

    # Convert list of tuples into normal list
    precip_lastyear = list(np.ravel(precip))

    # JSONIFY the object
    return jsonify(precip_lastyear)

# Stations route
@app.route("/api/v1.0/stations")
def stations():
    # Start the session for the page
    session = Session(engine)

    # Query Station sqlite and get all station names 
    station_names = session.query(Station.name).all()
    
    # Convert list of tuples into normal list
    all_stations = list(np.ravel(station_names))

    # JSONIFY the list of tuples
    return jsonify(all_stations)

# Temperature route
@app.route("/api/v1.0/tobs")
def temps():
    # Start the session for the page
    session = Session(engine)

    # Query Measurement sqlite to get the date and temperature
    temps = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > '2016-08-22').order_by(Measurement.date).all()

    # Create a list of a collection of dictionaries that extracts the data we want from the object
    temps_lastyear = []
    for date, tobs in temps:
        temp_dict = {}
        temp_dict["date"] = date
        temp_dict["tobs"] = tobs
        temps_lastyear.append(temp_dict)

    # JSONIFY the list
    return jsonify(temps_lastyear)

# Start date only route
@app.route("/api/v1.0/<start_date>")
def startDate(start_date):
    # Start the session for the page
    session = Session(engine)

    # Query Measurement sqlite to get the min, max and avg result for the selected date ranges 
    start_date = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()

    # JSONIFY the object
    return jsonify(start_date)

# Start and end date route
@app.route("/api/v1.0/<start_date>/<end_date>")
def startAndEndDate(start_date, end_date):
    # Start the session for the page
    session = Session(engine)

    # Query Measurement sqlite to get the min, max and avg result for the selected date ranges    
    start_and_end_date = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    # JSONIFY the object
    return jsonify(start_and_end_date)

# Allow for page debugging / log
if __name__ == '__main__':
    app.run(debug=True)

#SC
