import database.query as q

##### USER #####
def updUser(db, data):
    status, err = q.updateUser(db, data)
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
