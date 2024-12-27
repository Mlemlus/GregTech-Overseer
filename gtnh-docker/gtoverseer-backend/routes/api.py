from flask import request, jsonify, Blueprint, g
import api.add as add
import api.get as get
import api.upd as upd
import api.dele as dele # damn you del
from data.database.class_db import db as Database
import sys

api_bp = Blueprint('api', __name__)

############ Frontend handling ############
##### Functions #####
def initAddAdmin(conn_params, admin_params):
    try:
        db = Database(conn_params)
        add.addUser(db, admin_params)
        return True, None
    except Exception as e:
        return False , str(e)
    finally:
        del db

####### NOT CRUD ####### - very creative
##### SERVER CONFIG #####
@api_bp.route('/api/get/server-config', methods=['GET']) # server config get
def apiGetServerConfig():
    try:
        return jsonify(get.getServerConfig())
    except Exception as e:
        print(f"GET /api/get/server-config: {e}", file=sys.stderr)
        return jsonify({'status':False, 'error': str(e)})

@api_bp.route('/api/update/server-config', methods=['POST']) # update user
def apiUpdateServerConfig():
    try:
        data = request.json
        return jsonify(upd.updServerConfig(data))
    except Exception as e:
        print(f"POST /api/update/server-config: {e}", file=sys.stderr)
        return jsonify({'status':False, 'error': str(e)})


####### CRUD #######
##### USER #####
@api_bp.route('/api/authenticate', methods=['POST']) # user login auth process
def apiAuth():
    try:
        data = request.json
        db = Database(g.conn_params) # open db connection
        return jsonify(get.loginProcess(db, data)) # returns dict with login info
    except Exception as e:
        print(f"POST /api/authenticate: {e}", file=sys.stderr)
        return jsonify({'status':False, 'error': str(e)})
    finally:
        del db

@api_bp.route('/api/add/user', methods=['POST']) # add user
def apiAddUser():
    try:
        data = request.json
        db = Database(g.conn_params) # open db connection
        return jsonify(add.addUser(db, data))
    except Exception as e:
        print(f"POST /api/add/user: {e}", file=sys.stderr)
        return jsonify({'status':False, 'error': str(e)})
    finally:
        del db

@api_bp.route('/api/get/users', methods=['GET']) # get all users
def apiGetUsers():
    try:
        db = Database(g.conn_params) # open db connection
        return jsonify(get.getUsers(db))
    except Exception as e:
        print(f"GET /api/get/users: {e}", file=sys.stderr)
        return jsonify({'status':False, 'error': str(e)})
    finally:
        del db

@api_bp.route('/api/get/user', methods=['POST']) # get user
def apiGetUser():
    try:
        data = request.json
        db = Database(g.conn_params) # open db connection
        return jsonify(get.getUser(db,data))
    except Exception as e:
        print(f"POST /api/get/user: {e}", file=sys.stderr)
        return jsonify({'status':False, 'error': str(e)})
    finally:
        del db

@api_bp.route('/api/update/user', methods=['POST']) # update user
def apiUpdateUser():
    try:
        data = request.json
        db = Database(g.conn_params) # open db connection
        return jsonify(upd.updUser(db, data))
    except Exception as e:
        print(f"POST /api/update/user: {e}", file=sys.stderr)
        return jsonify({'status':False, 'error': str(e)})
    finally:
        del db

@api_bp.route('/api/delete/user', methods=['POST']) # delete user
def apiDeleteUser():
    try:
        data = request.json
        db = Database(g.conn_params) # open db connection
        return jsonify(dele.delUser(db, data))
    except Exception as e:
        print(f"POST /api/delete/user: {e}", file=sys.stderr)
        return jsonify({'status':False, 'error': str(e)})
    finally:
        del db

##### MACHINE #####
@api_bp.route('/api/get/machines', methods=['GET']) # get all machines
def apiGetMachines():
    try:
        db = Database(g.conn_params) # open db connection
        return jsonify(get.getMachines(db))
    except Exception as e:
        print(f"GET /api/get/machines: {e}", file=sys.stderr)
        return jsonify({'status':False, 'error': str(e)})
    finally:
        del db

@api_bp.route('/api/search/machines', methods=['POST']) # get searched machines
def apiSearchMachines():
    try:
        data = request.json
        db = Database(g.conn_params) # open db connection
        return jsonify(get.searchMachines(db,data))
    except Exception as e:
        print(f"POST /api/search/machines: {e}", file=sys.stderr)
        return jsonify({'status':False, 'error': str(e)})
    finally:
        del db

@api_bp.route('/api/update/machine', methods=['POST']) # update machine
def apiUpdateMachine():
    try:
        data = request.json
        db = Database(g.conn_params) # open db connection
        return jsonify(upd.updMachine(db, data))
    except Exception as e:
        print(f"POST /api/update/machine: {e}", file=sys.stderr)
        return jsonify({'status':False, 'error': str(e)})
    finally:
        del db


##### POWER NETWORK #####
@api_bp.route('/api/get/power-network-names', methods=['GET']) # get all PN names
def apiGetPowerNetworkNames():
    try:
        db = Database(g.conn_params) # open db connection
        return jsonify(get.getPowerNetworkNames(db))
    except Exception as e:
        print(f"GET /api/get/power-network-names: {e}", file=sys.stderr)
        return jsonify({'status':False, 'error': str(e)})
    finally:
        del db

@api_bp.route('/api/add/power-network', methods=['POST']) # add poewr network
def apiAddPowerNetwork():
    try:
        data = request.json
        db = Database(g.conn_params) # open db connection
        return jsonify(add.addPN(db, data))
    except Exception as e:
        print(f"POST /api/add/power-network: {e}", file=sys.stderr)
        return jsonify({'status':False, 'error': str(e)})
    finally:
        del db

@api_bp.route('/api/get/power-networks', methods=['GET']) # get all pns
def apiGetPowerNetworks():
    try:
        db = Database(g.conn_params) # open db connection
        return jsonify(get.getPNs(db))
    except Exception as e:
        print(f"GET /api/get/power-networks: {e}", file=sys.stderr)
        return jsonify({'status':False, 'error': str(e)})
    finally:
        del db

@api_bp.route('/api/update/power-network', methods=['POST']) # update power network
def apiUpdatePowerNetwork():
    try:
        data = request.json
        db = Database(g.conn_params) # open db connection
        return jsonify(upd.updPN(db, data))
    except Exception as e:
        print(f"POST /api/update/cable: {e}", file=sys.stderr)
        return jsonify({'status':False, 'error': str(e)})
    finally:
        del db

@api_bp.route('/api/delete/power-network', methods=['POST']) # delete PN
def apiDeletePowerNetwork():
    try:
        data = request.json
        db = Database(g.conn_params) # open db connection
        return jsonify(dele.delPN(db, data))
    except Exception as e:
        print(f"POST /api/delete/power-network: {e}", file=sys.stderr)
        return jsonify({'status':False, 'error': str(e)})
    finally:
        del db


##### CABLE #####
@api_bp.route('/api/add/cable', methods=['POST']) # add cable
def apiAddCable():
    try:
        data = request.json
        db = Database(g.conn_params) # open db connection
        return jsonify(add.addCable(db, data))
    except Exception as e:
        print(f"POST /api/add/cable: {e}", file=sys.stderr)
        return jsonify({'status':False, 'error': str(e)})
    finally:
        del db

@api_bp.route('/api/get/cables', methods=['GET']) # get all cables
def apiGetCables():
    try:
        db = Database(g.conn_params) # open db connection
        return jsonify(get.getCables(db))
    except Exception as e:
        print(f"GET /api/get/cables: {e}", file=sys.stderr)
        return jsonify({'status':False, 'error': str(e)})
    finally:
        del db

@api_bp.route('/api/get/cable-names', methods=['GET']) # get all cable names
def apiGetCableNames():
    try:
        db = Database(g.conn_params) # open db connection
        return jsonify(get.getCableNames(db))
    except Exception as e:
        print(f"GET /api/get/cable-names: {e}", file=sys.stderr)
        return jsonify({'status':False, 'error': str(e)})
    finally:
        del db

@api_bp.route('/api/update/cable', methods=['POST']) # update cable
def apiUpdateCable():
    try:
        data = request.json
        db = Database(g.conn_params) # open db connection
        return jsonify(upd.updCable(db, data))
    except Exception as e:
        print(f"POST /api/update/cable: {e}", file=sys.stderr)
        return jsonify({'status':False, 'error': str(e)})
    finally:
        del db

@api_bp.route('/api/delete/cable', methods=['POST']) # delete cable
def apiDeleteCable():
    try:
        data = request.json
        db = Database(g.conn_params) # open db connection
        return jsonify(dele.delCable(db, data))
    except Exception as e:
        print(f"POST /api/delete/cable: {e}", file=sys.stderr)
        return jsonify({'status':False, 'error': str(e)})
    finally:
        del db


##### TIER #####
@api_bp.route('/api/get/tier-names', methods=['GET']) # get all Tier names
def apiGetTierNames():
    try:
        db = Database(g.conn_params) # open db connection
        return jsonify(get.getTierNames(db))
    except Exception as e:
        print(f"GET /api/get/tier-names: {e}", file=sys.stderr)
        return jsonify({'status':False, 'error': str(e)})
    finally:
        del db

##### POWER SOURCE #####
@api_bp.route('/api/add/power-source', methods=['POST']) # add power source
def apiAddPowerSource():
    try:
        data = request.json
        db = Database(g.conn_params) # open db connection
        return jsonify(add.addPS(db, data))
    except Exception as e:
        print(f"POST /api/add/power-source: {e}", file=sys.stderr)
        return jsonify({'status':False, 'error': str(e)})
    finally:
        del db

@api_bp.route('/api/get/power-sources', methods=['GET']) # get all power sources
def apiGetPowerSources():
    try:
        db = Database(g.conn_params) # open db connection
        return jsonify(get.getPSs(db))
    except Exception as e:
        print(f"GET /api/get/power-sources: {e}", file=sys.stderr)
        return jsonify({'status':False, 'error': str(e)})
    finally:
        del db

@api_bp.route('/api/get/power-source', methods=['POST']) # get power source
def apiGetPowerSource():
    try:
        data = request.json
        db = Database(g.conn_params) # open db connection
        return jsonify(get.getPS(db,data))
    except Exception as e:
        print(f"GET /api/get/power-source: {e}", file=sys.stderr)
        return jsonify({'status':False, 'error': str(e)})
    finally:
        del db

@api_bp.route('/api/update/power-source', methods=['POST']) # update power source
def apiUpdatePowerSource():
    try:
        data = request.json
        db = Database(g.conn_params) # open db connection
        return jsonify(upd.updPS(db, data))
    except Exception as e:
        print(f"POST /api/update/power-source: {e}", file=sys.stderr)
        return jsonify({'status':False, 'error': str(e)})
    finally:
        del db

@api_bp.route('/api/delete/power-source', methods=['POST']) # delete PS
def apiDeletePowerSource():
    try:
        data = request.json
        db = Database(g.conn_params) # open db connection
        return jsonify(dele.delPS(db, data))
    except Exception as e:
        print(f"POST /api/delete/power-source: {e}", file=sys.stderr)
        return jsonify({'status':False, 'error': str(e)})
    finally:
        del db