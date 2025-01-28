from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import datetime as dt
import numpy as np

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
Base.prepare(engine, reflect=True)

# save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session to grab data needed for global variables
session = Session(engine)

# 1) Get the most recent date in the dataset
most_recent_date = session.query(Measurement.date)\
    .order_by(Measurement.date.desc()).first()[0]

# 2) Find the most active station
active_stations = (session.query(Measurement.station, func.count(Measurement.station))
                   .group_by(Measurement.station)
                   .order_by(func.count(Measurement.station).desc())
                   .all())
most_active_station = active_stations[0][0]  # e.g. "USC00519281"

session.close()


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available API routes."""
    return (
        f"<h1>Welcome to the Hawaii Climate API</h1>"
        f"<h2>Available Routes:</h2>"
        f'<a href="/api/v1.0/precipitation">/api/v1.0/precipitation</a><br/>'
        f'<a href="/api/v1.0/stations">/api/v1.0/stations</a><br/>'
        f'<a href="/api/v1.0/tobs">/api/v1.0/tobs</a><br/><br/>'
        f"For these routes, replace the date parts with YYYY-MM-DD:<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a JSON dictionary of date -> precipitation for the last year."""
    session = Session(engine)
    one_year_ago = dt.datetime.strptime(most_recent_date, '%Y-%m-%d') - dt.timedelta(days=365)

    results = (session.query(Measurement.date, Measurement.prcp)
               .filter(Measurement.date >= one_year_ago)
               .all())
    session.close()

    # Convert list of tuples into dict {date: prcp}
    precip_dict = {date: prcp for date, prcp in results}
    return jsonify(precip_dict)

@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of station IDs."""
    session = Session(engine)
    results = session.query(Station.station).all()
    session.close()

    stations_list = list(np.ravel(results))
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a JSON list of temp observations of the most active station for the last year."""
    session = Session(engine)
    one_year_ago = dt.datetime.strptime(most_recent_date, '%Y-%m-%d') - dt.timedelta(days=365)

    results = (session.query(Measurement.date, Measurement.tobs)
               .filter(Measurement.station == most_active_station)
               .filter(Measurement.date >= one_year_ago)
               .all())
    session.close()

    # Return a list of dicts for clarity
    tobs_data = []
    for date, temp in results:
        tobs_data.append({"date": date, "temperature": temp})
    return jsonify(tobs_data)

@app.route("/api/v1.0/<start>")
def start_only(start):
    """
    Return min, max, and average temperature for all dates >= start.
    Example: /api/v1.0/2016-08-23
    """
    session = Session(engine)
    results = (session.query(func.min(Measurement.tobs),
                             func.max(Measurement.tobs),
                             func.avg(Measurement.tobs))
               .filter(Measurement.date >= start)
               .all())
    session.close()

    temps = list(np.ravel(results))
    return jsonify(temps)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    """
    Return min, max, and average temperature for dates between start and end (inclusive).
    Example: /api/v1.0/2016-08-23/2017-08-23
    """
    session = Session(engine)
    results = (session.query(func.min(Measurement.tobs),
                             func.max(Measurement.tobs),
                             func.avg(Measurement.tobs))
               .filter(Measurement.date >= start)
               .filter(Measurement.date <= end)
               .all())
    session.close()

    temps = list(np.ravel(results))
    return jsonify(temps)

if __name__ == "__main__":
    app.run(debug=True)