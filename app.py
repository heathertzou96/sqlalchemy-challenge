import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()

Measurement = Base.classes.measurement
Station = Base.classes.station

#Flask Setup
app = Flask(__name__)

#Flask Routes
@app.route("/")
def home_page():
    return (
        f"Welcome to the Home Page<br/>"
        f"Here are the available routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f" TEMPERATURE ONE HERE"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()

    all_prcp = []
    for date, prcp in results:
        prcp_dict = {date:prcp}
        
        #prcp_dict["date"] = date
        #prcp_dict["prcp"] = prcp

        all_prcp.append(prcp_dict)
    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.station).all()
    session.close()

    all_station = []
    station_count = 1
    for station in results:
        station_dict = {f"station{station_count}":station}

        #station_dict = {}
        #station_dict["station"] = station
        
        all_station.append(station_dict)
        station_count += 1
    return jsonify(all_station)



if __name__ == "__main__":
    app.run(debug=True)
