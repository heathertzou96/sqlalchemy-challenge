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
        f"<h3>Welcome to the Home Page</h3>"
        f"Here are the available routes:<br/>"
        f"<a href = '/api/v1.0/precipitation' target='_blank'>/api/v1.0/precipitation</a><br/>"
        f"<a href = '/api/v1.0/stations' target='_blank'>/api/v1.0/stations</a><br/>"
        f"<a href = '/api/v1.0/tobs' target='_blank'>/api/v1.0/tobs</a><br/>"
        f"<a href = '/api/v1.0/2017-08-15' target= '_blank'>/api/v1.0/2017-08-15</a><br/>"
        f"<a href = '/api/v1.0/2017-08-15/2017-08-20' target= '_blank'>/api/v1.0/2017-08-15/2017-08-20</a>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()

    all_prcp = []
    for date, prcp in results:
        prcp_dict = {date:prcp}
        all_prcp.append(prcp_dict)
    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.station).all()
    session.close()

    all_station = []
    station_count = 1 #used this counter mainly to differentiate the different stations for its key values
    for station in results:
        station_dict = {f"station{station_count}":station}
        all_station.append(station_dict)
        station_count += 1
    return jsonify(all_station)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= '2016-08-23').\
        filter(Measurement.station == "USC00519281").\
        order_by(Measurement.tobs).all()
    session.close()

    all_tobs = []
    for date, tobs in results:
        tobs_dict = {date:tobs}
        all_tobs.append(tobs_dict)
    return jsonify(all_tobs)

@app.route("/api/v1.0/2017-08-15")
def start():
    session = Session(engine)
    
    min_temp = session.query(func.min(Measurement.tobs)).\
        filter(Measurement.date >= "2017-08-15").all()

    avg_temp = session.query(func.avg(Measurement.tobs)).\
        filter(Measurement.date >= "2017-08-15").all()

    max_temp = session.query(func.max(Measurement.tobs)).\
        filter(Measurement.date >= "2017-08-15").all()

    start_list = [min_temp, avg_temp, max_temp]
    
    session.close()

    all_start = []
    start_dict = {}
    start_dict["minimum temperature"] = start_list[0]
    start_dict["average temperature"] = start_list[1]
    start_dict["maximum temperature"] = start_list[2]
    all_start.append(start_dict)

    return jsonify(all_start)

@app.route("/api/v1.0/2017-08-15/2017-08-20")
def start_end():
    session = Session(engine)
    
    min_temp = session.query(func.min(Measurement.tobs)).\
        filter(Measurement.date >= "2017-08-15").\
        filter(Measurement.date <= "2017-08-20").all()

    avg_temp = session.query(func.avg(Measurement.tobs)).\
        filter(Measurement.date >= "2017-08-15").\
        filter(Measurement.date <= "2017-08-20").all()

    max_temp = session.query(func.max(Measurement.tobs)).\
        filter(Measurement.date >= "2017-08-15").\
        filter(Measurement.date <= "2017-08-20").all()

    start_end_list = [min_temp, avg_temp, max_temp]
    
    session.close()

    all_start_end = []
    start_end_dict = {}
    start_end_dict["minimum temperature"] = start_end_list[0]
    start_end_dict["average temperature"] = start_end_list[1]
    start_end_dict["maximum temperature"] = start_end_list[2]
    all_start_end.append(start_end_dict)

    return jsonify(all_start_end)

if __name__ == "__main__":
    app.run(debug=True)

