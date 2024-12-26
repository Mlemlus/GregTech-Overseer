import database.query as q

##### USER #####
def addUser(db, data):
    status, err = q.insUser(db, data)
    return{"status":status, "error":err}

##### CABLE #####
def addCable(db, data):
    status, err = q.insCable(db, data)
    return{"status":status, "error":err}

##### POWER NETWORK #####
def addPN(db, data):
    status, err = q.insPowerNetwork(db,data)
    return{"status":status, "error":err}

##### POWER SOURCE #####
def addPS(db, data):
    status, err = q.insPowerSourceManual(db,data)
    return{"status":status, "error":err}