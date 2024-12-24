import database.query as q

##### USER #####
def updUser(db, old_username, username, email):
    q.updateUser(db, {"old_username":str(old_username), "username": str(username), "email": str(email)})
    return {'status':True}

##### MACHINE #####
def updMachine(db, ID, name, pnname, chunkloaded, note):
    if not pnname or pnname == "None":
        pnname = "NULL"
    q.updateMachine(
        db,
        {
            "ID":str(ID),
            "name":str(name),
            "pnname":str(pnname),
            "chunkloaded":chunkloaded,
            "note":str(note)
        })
    return {'status':True}

