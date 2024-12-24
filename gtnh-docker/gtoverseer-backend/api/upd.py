import database.query as q

##### USER #####
def updUser(db, old_username, username, email):
    q.updateUser(db, {"old_username":str(old_username), "username": str(username), "email": str(email)})
    return {'status':True}
