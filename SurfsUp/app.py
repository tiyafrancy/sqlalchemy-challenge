# Import the dependencies.
from flask import Flask, jsonify
from sqlalchemy import create_engine, func, desc
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from datetime import datetime, timedelta


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with = engine)

# Save references to each table
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

# Home Page
@app.route("/")
def home():
    return (
        f"Welcome to the Climate App Home Page <br>"
        f"Available Routes: <br>"
        f"Precipitation : /api/v1.0/precipitation <br>"
        f"List of Stations : /api/v1.0/stations <br>"
        f"Temperature observations of the most-active station : /api/v1.0/tobs <br>"
        f"Temperature statistics from the start : /api/v1.0/<start> <br>"
        f"Temperature statistics from start date to the end date : /api/v1.0/<start>/<end> <br>"
        )

# Collecting precipitation data
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Starting from the most recent data point in the database
    most_recent_date_points = session.query(Measurement.date).order_by(desc(Measurement.date)).first()

    # Calculate the date one year from the last date in data set
    most_recent_date = datetime.strptime(most_recent_date_points[0], "%Y-%m-%d")    # converting to required date format

    latest_date = (most_recent_date) - timedelta(days = 366)

    # Perform a query to retrieve the data and precipitation scores
    precipitation = session.query(Measurement.date, Measurement.prcp).\
                                filter(Measurement.date >= latest_date).\
                                all()
    
    precipitation_dict = {}
    for date, prcp in precipitation:
        precipitation_dict[date] = prcp
    
    return jsonify(precipitation_dict)


# Collecting station data
@app.route("/api/v1.0/stations")
def stations():
    station_data = session.query(Measurement.station).distinct().all()
    station_list = []
    for station in station_data:
        station_list.append(station[0])
    return jsonify(station_list)


# Collecting temperature data
@app.route("/api/v1.0/tobs")
def tobs():
    most_active_station_id = "USC00519281"

    # Starting from the most recent data point in the database
    most_recent_date_points = session.query(Measurement.date).order_by(desc(Measurement.date)).first()

    # Calculate the date one year from the last date in data set
    most_recent_date = datetime.strptime(most_recent_date_points[0], "%Y-%m-%d")    # converting to required date format

    latest_date = (most_recent_date) - timedelta(days = 366)

    temperature_data = session.query(Measurement.tobs).\
                                    filter(Measurement.station == most_active_station_id).\
                                    filter(Measurement.date >= latest_date).\
                                    filter(Measurement.date <= most_recent_date).\
                                    all()

    tobs_list = []
    for tobs in temperature_data:
        tobs_list.append(tobs[0])

    return jsonify(tobs_list)



# Collecting temperature data from a start date
@app.route("/api/v1.0/<start>")
def get_start_date(start):
    data = session.query(func.min(Measurement.tobs),
                        func.avg(Measurement.tobs),
                        func.max(Measurement.tobs)).\
                        filter(Measurement.date >= start).all()
    if data:
        return jsonify({"TMIN": data[0][0],
                        "TAVG": data[0][1],
                        "TMAX": data[0][2]})
    else:
        return jsonify({"error": "No data found for the given start date."}), 404
    

# Collecting temperature data from start to end date
@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    data = session.query(func.min(Measurement.tobs),
                        func.avg(Measurement.tobs),
                        func.max(Measurement.tobs)).\
                        filter(Measurement.date >= start).\
                        filter(Measurement.date <= end).\
                        all()
    if data:
        return jsonify({"TMIN": data[0][0],
                        "TAVG": data[0][1],
                        "TMAX": data[0][2]})
    else:
        return jsonify({"error": "No data found for the given start date."}), 404
    

if __name__ == "__main__":
    app.run(debug = True)