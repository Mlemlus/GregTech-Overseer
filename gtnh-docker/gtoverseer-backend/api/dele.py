import database.query as q

##### USER #####
def delUser(db, username):
    q.deleteUser(db, {"username": str(username)})
    return {'status':True}
