from flask import request, Blueprint, g, jsonify
from data.database.class_db import db as Database
import sys, shared as s, datetime as dt, requests
from data.data_process.data_parse import parseIntialData
from data.data_process.data_processes import insRestart, updWork, logStatus, getLogStatus

data_bp = Blueprint("data", __name__)

############ Open Computers handling ############
# How to interact with gto_controller
# The controller is severely limited in everything, so the less processing it has to do the better
# It returns all responses in json ###(prob should just get raw and process it here)
# And awaits for a command in form of: str(3_digits_task) + str(optional_data)
# It extracts the task and acts accordingly
# Tasks, if successful returns same code 
#   100 - Update all working GT machines work progress
#   204 - Initialize configuration
#   205 - Reinitialize all connected GT machines
#   400 - No data recieved, #######print error on screen and pause
#   500 - Server error


@data_bp.route("/data", methods=["POST"]) # Route to handle OC data POST requests
def handleDataRequest():
    data = request.json
    if not data:
        return "400"
    override_task = None
    oc_address = data["oc_address"]
    # use the recieved data based on the status code
    try:
        db = Database(g.conn_params)
        match data["status"]:
            case "100": # update progress
                if not updWork(db, data["data"]):
                    override_task = "205"
            case "204": # config reset confirmation
                s.oc_stations[oc_address]["latest_config"] = True
            case "205": # data reset
                parsed_data = parseIntialData(data["data"])
                if not insRestart(db, parsed_data):
                    override_task = "205" #### prob should return something else
                s.oc_stations[oc_address] = { # register oc station for backend
                    "last_response":dt.datetime.now(),
                    "last_reset":dt.datetime.now(),
                    "latest_config": False
                    }
                override_task = "204" + resetConfig() # Sends new config

    except Exception as e:
        requests.post("http://10.21.31.5:40649/log",json={
                "text":f"handleDataRequest: {e}"
            })
        return "500" + f"handleDataRequest: {e}"
    # if one of the status tasks failed, the next task gets overriden
    if override_task != None:
        return override_task

    # check if we got the station registered
    if not oc_address in s.oc_stations:
        return "205"

    # update last_response
    s.oc_stations[oc_address]["last_response"] = dt.datetime.now()

    # Check if it's time to reinitialize
    if dt.datetime.now() - s.oc_stations[oc_address]["last_reset"] > dt.timedelta(minutes=s.oc_stations_reinitialization_rate):
        return "205"

    # Check if newer configuration is avaliable
    if not s.oc_stations[oc_address]["latest_config"]:
        return "204" + resetConfig() # Sends new config

    # And if everyting works out just update work data
    return "100"


def resetConfig(): # returns OC station configuration string
    # To keep it minimal we will only send values separated by ,
    # the controller knows the order of values
    config_string = []
    config_string.append(s.oc_stations_update_rate)
    return ",".join(str(val) for val in config_string) # pog

############ Log handling ############
@data_bp.route("/log", methods=["POST"]) # logs incoming data
def handlePostLogStatus():
    try:
        data = request.json
        db = Database(g.conn_params) # open db connection
        return jsonify(logStatus(db, data))
    except Exception as e:
        print(f"POST /log: {e}", file=sys.stderr) # who reports the reporter?
        return jsonify({'status':False, 'error': str(e)})
    finally:
        del db

@data_bp.route("/log", methods=["GET"]) # returns logs
def handleGetLogStatus():
    try:
        db = Database(g.conn_params) # open db connection
        return jsonify(getLogStatus(db))
    except Exception as e:
        print(f"GET /log: {e}", file=sys.stderr) # who reports the reporter?
        return jsonify({'status':False, 'error': str(e)})
    finally:
        del db
