import data.database.query as q

##### USER #####
def delUser(db, data):
    status, err = q.deleteUser(db, data)
    return {"status":status, "error":err}

##### CABLE #####
def delCable(db, data):
    status, err = q.deleteCable(db, data)
    return {"status":status, "error":err}

##### POWER NETWORK #####
def delPN(db, data):
    status, err = q.deletePowerNetwork(db, data)
    return {"status":status, "error":err}

##### POWER SOURCE #####
def delPS(db, data):
    status, err = q.deletePowerSource(db, data)
    return {"status":status, "error":err}