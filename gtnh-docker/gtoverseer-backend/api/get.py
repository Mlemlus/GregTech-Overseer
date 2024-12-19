import database.query as q
import sys ################

def loginProcess(db, email, password):
    username = q.selUserEmailPassword(db, {"email": str(email), "password": str(password)})
    # priviliges and stuff can be returned from here
    #   *futureproofing*
    if username:
        return {'status':True, 'username':username[0]}
    else:
        return {'status':False, 'username':""}
    