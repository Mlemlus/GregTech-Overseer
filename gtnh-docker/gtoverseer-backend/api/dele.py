import database.query as q

##### USER #####
def delUser(db, username):
    q.deleteUser(db, {"username": str(username)})
    return {'status':True}

##### CABLE #####
def delCable(db, name):
    q.deleteCable(db, {"name": str(name)})
    return {'status':True}

##### POWER NETWORK #####
def delPN(db, data):
    q.deletePowerNetwork(db, data)
    return {'status':True}

##### POWER SOURCE #####
def delPS(db, data):
    q.deletePowerSource(db, data)
    return {'status':True}


