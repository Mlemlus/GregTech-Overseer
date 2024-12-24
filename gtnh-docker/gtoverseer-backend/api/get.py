import database.query as q
import sys ################

##### USER #####
def loginProcess(db, email, password):
    username = q.selUserEmailPassword(db, {"email": str(email), "password": str(password)})
    # priviliges and stuff can be returned from here
    #   *futureproofing*
    if username:
        return {'status':True, 'username':username[0]}
    else:
        return {'status':False, 'username':""}

def getUsers(db):
    users = q.selAllUsers(db)   
    if users:
        return {'status':True, 'users':users}
    else:
        return {'status':False, 'users':{"upsieWoopsie"}}
    
def getUser(db, username):
    user = q.selUserUsername(db, username)
    if user:
        return {'status':True, 'user':user}
    else:
        return {'status':False, 'user':{}}

def searchUsers(db, search_term):
    users = q.searchUsers(db, {"search": str(search_term)})
    if users:
        return {'status':True, 'users':users}
    else:
        return {'status':False, 'users':{}}
