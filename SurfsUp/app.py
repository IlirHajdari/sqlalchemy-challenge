# Import the dependencies.
from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import datetime as dt
import numpy as np

app = Flask(__name__)


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# Get most recent date from dataset
most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]

# Close session
session.close()

#################################################
# Flask Setup
#################################################
@app.route("/")
def welcome():
    return (
        f"Welcome to the Hawaii Climate API<br/>"
        f"Here Are All Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )





#################################################
# Flask Routes
#################################################

@app.route("/api/v1.0/precipitation")
def precipitation():

    # Session to DB
    session = Session(engine)

    # Calc date for one year ago from the last date in the dataset
    one_year_ago = dt.datetime.strptime(most_recent_date, '%Y-%m-%d') - dt.timedelta(days=365)

    # Preform query that retrieves data and precipitation scores
    precipitation_data = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= one_year_ago).all()
    
    # Close session
    session.close()


    precipitation_dict = {date: prcp for date, prcp in precipitation_data}
    return jsonify(precipitation_dict)


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    results = session.query(Station.station).all()

    session.close()

    stations = list(np.ravel(results))
    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    one_year_ago = dt.datetime.strptime(most_recent_date, '%Y-%m-%d') - dt.timedelta(days=365)

    temperature_data = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active_station).\
        filter(Measurement.date >= one_year_ago).all()
    
    session.close()

    temperatures = list(np.ravel(temperature_data))
    return jsonify(temperatures)

@app.route("/api/v1.0/<start>")
def start(start):
	session = Session(engine)

	results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
		filter(Measurement.date >= start).all()

	session.close()

	temperature = list(np.ravel(results))
	return jsonify(temps)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
	session = Session(engine)

	results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
		filter(Measurement.date >= start).filter(Measurement.date <= end).all()

	session.close()

	temps = list(np.ravel(results))
	return jsonify(temps)
		

if __name__ == "__main__":
    app.run(debug=True)