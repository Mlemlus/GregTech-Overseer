import data.database.query as q, shared as s

##### USER #####
def updUser(db, data):
    status, err = q.updateUser(db, data)
    q.deleteUserPrivilege(db,data)
    for priv in data["privileges"]:
        q.insUserPrivilege(db,
            {"username":data["username"],
             "privilege":priv})
    return {"status":status, "error":err}

def updUserPassword(db, data):
    status, err = q.updateUserPassword(db, data)
    return {"status":status, "error":err}

##### MACHINE #####
def updMachine(db, data):
    if not data["pnname"] or data["pnname"] == "None": # rewrite None to SQL NULL
        data["pnname"] = "NULL" 
    status, err = q.updateMachine(db, data)
    return {"status":status, "error":err}

##### CABLE #####
def updCable(db, data):
    status, err = q.updateCable(db, data)
    return {"status":status, "error":err}

##### POWER NETWORK #####
def updPN(db, data):
    status, err = q.updatePowerNetwork(db, data)
    return {"status":status, "error":err}

##### POWER SOURCE #####
def updPS(db, data):
    status, err = q.updatePowerSource(db, data)
    return {"status":status, "error":err}

##### SERVER CONFIG #####
def updServerConfig(data):
    s.oc_stations_update_rate = data["oc_stations_update_rate"]/1000
    s.oc_stations_reinitialization_rate = data["oc_stations_reinitialization_rate"]
    for station in s.oc_stations:
        s.oc_stations[station]["latest_config"] = False
    return {"status":True}