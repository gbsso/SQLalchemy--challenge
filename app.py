# Dependencies
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite",
                        connect_args={"check_same_thread": False})

Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

latest_date = (session.query(Measurement.date).order_by(Measurement.date.desc()).first())

latest_date = list(np.ravel(latest_date))[0]

latest_date = dt.datetime.strptime(latest_date, '%Y-%m-%d')
latest_year = int(dt.datetime.strftime(latest_date, '%Y'))
latest_month = int(dt.datetime.strftime(latest_date, '%m'))
latest_date = int(dt.datetime.strftime(latest_date, '%d'))

yearBefore = dt.date(latest_year, latest_month, latest_date) - dt.timedelta(days=365)
precipitation_scores = (session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > yearBefore)
            .order_by(Measurement.date).all())

# Climate app
app = Flask(__name__)


@app.route("/")
def home():
    return (f"SQLAlchemy Homework - Surfs Up!<br/>"
            f"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~<br/>"
            f"Available Routes:<br/>"
            f"/api/v1.0/precipitaton ~~ preceipitation data<br/>"
            f"/api/v1.0/stations ~~~~~ weather observation stations<br/>"
            f"/api/v1.0/temperature ~~ temperature data<br/>"
            f"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~<br/>")
            
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.name).all()
    active_stations = list(np.ravel(results))
    return jsonify(active_stations)

@app.route("/api/v1.0/precipitaton")
def precipitation():
    
    results = (session.query(Measurement.date, Measurement.prcp, Measurement.station)
                      .filter(Measurement.date > yearBefore)
                      .order_by(Measurement.date)
                      .all())
    
    precipitation_data = []
    for result in results:
        precipitation_dict = {result.date: result.prcp, "Station": result.station}
        precipitation_data.append(precipitation_dict)

    return jsonify(precipitation_data)

@app.route("/api/v1.0/temperature")
def temperature():

    results = (session.query(Measurement.date, Measurement.tobs, Measurement.station)
                      .filter(Measurement.date > yearBefore)
                      .order_by(Measurement.date)
                      .all())

    temperature_data = []
    for result in results:
        temperature_dict = {result.date: result.tobs, "Station": result.station}
        temperature_data.append(temperature_dict)

    return jsonify(temperature_data)





























if __name__ == "__main__":
    app.run(debug=True)
