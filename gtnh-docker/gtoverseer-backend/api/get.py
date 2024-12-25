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
    
##### MACHINE #####
def getMachines(db):
    machines = q.machineReport(db)
    if machines:
        return {'status':True, 'machines':machines}
    else:
        return {'status':False, 'machines':{"upsieWoopsie"}}


##### POWER NETWORK #####
def getPowerNetworkNames(db):
    power_networks = q.selAllNetowrksNames(db)
    if power_networks:
        return {'status':True, 'pnnames':power_networks}
    else:
        return {'status':False, 'pnnames':{"upsieWoopsie"}}

##### CABLE #####
def getCables(db):
    cables = q.selAllCables(db)
    if cables:
        return {'status':True, 'cables':cables}
    else:
        return {'status':False, 'cables':{"upsieWoopsie"}}

##### TIER #####
def getTierNames(db):
    tiers = q.selAllTierNames(db)
    if tiers:
        return {'status':True, 'tiers':tiers}
    else:
        return {'status':False, 'tiers':{"upsieWoopsie"}}
