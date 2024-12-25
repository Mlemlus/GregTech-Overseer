import database.query as q

##### USER #####
def delUser(db, username):
    q.deleteUser(db, {"username": str(username)})
    return {'status':True}

##### CABLE #####
def delCable(db, name):
    q.deleteCable(db, {"name": str(name)})
    return {'status':True}
