from flask import Flask, request, jsonify
from database.class_db import db as Database
import json, uuid, os
from data_process.data_parse import parseIntialData
from data_process.data_processes import insRestart, updWork
import sys #######################
import database.query as q ############

app = Flask(__name__)

def actionStatus(response): # Responds based on the recieved HTTP response status code
    match response['status']:
        case '100': # update machines status data
            updateWorkData(response['data'])
            return "100", "UPDATE"
        case '205': # data reset confirmation
            return resetUpdate(response['data'])

def updateWorkData(data):
    try:
        db = Database(conn_params) # open db connection
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
        db = Database(conn_params) # open db connection
        if insRestart(db, data):
            return "100", str(uuid.uuid4())  # returns a new session_id with the status
        else: 
            return "205", "CORRUPTED DATA" # resend data
    except Exception as e:
        print(f"resetUpdate: failed to respond: {e}", file=sys.stderr)
        return "500", e
    finally:
        del db # close the connection


# Route to handle POST requests
@app.route('/data', methods=['POST'])
def handlePostRequest():    
    # Process the data in some way (for now, just check if we got any data)
    data = request.data
    if isinstance(data, bytes):
        data = str(data.decode('utf-8'))
        data = json.loads(data)

    if data:
        status, response = actionStatus(data)
    else:
        status, response = 400, "No recieved data"

    
    # Send back a response
    return status + response

@app.route('/data', methods=['GET'])
def handleGetRequest():
    data = {}
    try:
        db = Database(conn_params) # open db connection
        return jsonify(q.machineReport(db))
    except Exception as e:
        print(f"GET /data: no database connection: {e}", file=sys.stderr)
        data = {'error': str(e)}
        return jsonify(data)
    finally:
        del db
    



if __name__ == '__main__':
    conn_params = {
        "dbname": os.getenv("DBNAME"),
        "user": os.getenv("USER"),
        "password": os.getenv("PASSWORD"),
        "host": os.getenv("HOST"),
        "port": os.getenv("PORT")
    }
    
    app.run(debug=True, host='0.0.0.0', port=40649)


