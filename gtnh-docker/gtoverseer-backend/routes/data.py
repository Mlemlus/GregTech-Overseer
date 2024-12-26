from flask import request, Blueprint, g
from data.database.class_db import db as Database
import json, uuid, sys
from data.data_process.data_parse import parseIntialData
from data.data_process.data_processes import insRestart, updWork

data_bp = Blueprint('data', __name__)

############ Open Computers handling ############
def actionStatus(response): # Responds based on the recieved HTTP response status code
    match response['status']:
        case '100': # update machines status data
            updateWorkData(response['data'])
            return "100", "UPDATE"
        case '205': # data reset confirmation
            return resetUpdate(response['data'])

def updateWorkData(data):
    try:
        db = Database(g.conn_params) # open db connection
        if updWork(db, data):
            return "100", "UPDATED"
        else:
            return "205", "CORRUPTED DATA"
    except Exception as e:
        print(f"updateWorkData: failed to update: {e}", file=sys.stderr)
        return "500", str(e)
    finally:
        del db # close the connection

def resetUpdate(raw_data):
    data = parseIntialData(raw_data)
    try:
        db = Database(g.conn_params) # open db connection
        if insRestart(db, data):
            return "100", str(uuid.uuid4())  # returns a new session_id with the status
        else: 
            return "205", "CORRUPTED DATA" # resend data
    except Exception as e:
        print(f"resetUpdate: failed to respond: {e}", file=sys.stderr)
        return "500", e
    finally:
        del db # close the connection


# Route to handle OC data POST requests
@data_bp.route('/data', methods=['POST'])
def handlePostRequest():    
    # Process the data in some way (for now, just check if we got any data)
    data = request.json
    if data:
        status, response = actionStatus(data)
    else:
        status, response = 400, "No recieved data"

    # Send back a response
    return status + response

