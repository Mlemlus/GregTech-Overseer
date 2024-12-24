from flask import Flask, request, jsonify
from database.class_db import db as Database
import json, uuid, os
from data_process.data_parse import parseIntialData
from data_process.data_processes import insRestart, updWork
import api.add as add
import api.get as get
import api.upd as upd
import api.dele as dele # damn you del
import sys

app = Flask(__name__)

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


# Route to handle OC data POST requests
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


############ Frontend handling ############
##### USER #####
@app.route('/api/authenticate', methods=['POST']) # user login auth process
def handleApiAuthRequest():
    try:
        data = request.json
        db = Database(conn_params) # open db connection
        response = get.loginProcess(db, data['email'], data['password'])
        return jsonify(response) # returns dict with login info
    except Exception as e:
        print(f"POST /api/authenticate: {e}", file=sys.stderr)
        data = {'error': str(e)}
        return jsonify(data)
    finally:
        del db

@app.route('/api/add/user', methods=['POST']) # add user
def handleApiAddUserRequest():
    data = request.data
    if isinstance(data, bytes):
        data = str(data.decode('utf-8'))
        data = json.loads(data)
    try:
        db = Database(conn_params) # open db connection
        add.addUser(db, data['username'], data['email'], data['password'])
        return jsonify({'status':True})
    except Exception as e:
        print(f"POST /api/add/user: {e}", file=sys.stderr)
        data = {'status':False, 'error': str(e)}
        return jsonify(data)
    finally:
        del db

@app.route('/api/get/users', methods=['GET']) # get all users
def handleApiGetUsersRequest():
    try:
        db = Database(conn_params) # open db connection
        return jsonify(get.getUsers(db))
    except Exception as e:
        print(f"GET /api/get/users: {e}", file=sys.stderr)
        data = {'status':False, 'error': str(e)}
        return jsonify(data)
    finally:
        del db

@app.route('/api/get/user', methods=['POST']) # get user
def handleApiGetUserRequest():
    data = request.data
    if isinstance(data, bytes):
        data = str(data.decode('utf-8'))
        data = json.loads(data)
    try:
        db = Database(conn_params) # open db connection
        return jsonify(get.getUser(db,data['username']))
    except Exception as e:
        print(f"POST /api/get/user: {e}", file=sys.stderr)
        data = {'status':False, 'error': str(e)}
        return jsonify(data)
    finally:
        del db

@app.route('/api/update/user', methods=['POST']) # update user
def handleApiUpdateUserRequest():
    data = request.data
    if isinstance(data, bytes):
        data = str(data.decode('utf-8'))
        data = json.loads(data)
    try:
        db = Database(conn_params) # open db connection
        return jsonify(upd.updUser(db, data['old_username'], data['username'], data['email']))
    except Exception as e:
        print(f"POST /api/update/user: {e}", file=sys.stderr)
        data = {'status':False, 'error': str(e)}
        return jsonify(data)
    finally:
        del db

@app.route('/api/delete/user', methods=['POST']) # delete user
def handleApiDeleteUserRequest():
    data = request.data
    if isinstance(data, bytes):
        data = str(data.decode('utf-8'))
        data = json.loads(data)
    try:
        db = Database(conn_params) # open db connection
        return jsonify(dele.delUser(db, data['username']))
    except Exception as e:
        print(f"POST /api/delete/user: {e}", file=sys.stderr)
        data = {'status':False, 'error': str(e)}
        return jsonify(data)
    finally:
        del db

##### MACHINE #####
@app.route('/api/get/machines', methods=['GET']) # get all machines
def handleApiGetMachinesRequest():
    try:
        db = Database(conn_params) # open db connection
        return jsonify(get.getMachines(db))
    except Exception as e:
        print(f"GET /api/get/machines: {e}", file=sys.stderr)
        data = {'status':False, 'error': str(e)}
        return jsonify(data)
    finally:
        del db

@app.route('/api/update/machine', methods=['POST']) # update machine
def handleApiUpdateMachineRequest():
    data = request.data
    if isinstance(data, bytes):
        data = str(data.decode('utf-8'))
        data = json.loads(data)
    try:
        db = Database(conn_params) # open db connection
        return jsonify(upd.updMachine(db, data['ID'], data['name'], data['pnname'], data['chunkloaded'], data['note']))
    except Exception as e:
        print(f"POST /api/update/machine: {e}", file=sys.stderr)
        data = {'status':False, 'error': str(e)}
        return jsonify(data)
    finally:
        del db


##### POWER NETWORK #####
@app.route('/api/get/power-network-names', methods=['GET']) # get all PN names
def handleApiGetPowerNetworkNamesRequest():
    try:
        db = Database(conn_params) # open db connection
        return jsonify(get.getPowerNetworkNames(db))
    except Exception as e:
        print(f"GET /api/get/power-network-names: {e}", file=sys.stderr)
        data = {'status':False, 'error': str(e)}
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
    
    # if we add the admin account every time, it has to exist (it gets updated on conflict)
    try:
        db = Database(conn_params) # open db connection
        add.addUser(db, os.getenv("ADMIN_USERNAME"),os.getenv("ADMIN_EMAIL"),os.getenv("ADMIN_PASSWORD"))
    except Exception as e:
        print(f"main: no database connection: {e}", file=sys.stderr)
    finally:
        del db

    app.run(debug=True, host='0.0.0.0', port=40649)