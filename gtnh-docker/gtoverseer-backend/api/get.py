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

def getPNs(db):
    pns = q.selAllPowerNetworks(db)
    if pns:
        return {'status':True, 'pns':pns}
    else:
        return {'status':False, 'pns':{"upsieWoopsie"}}

##### CABLE #####
def getCables(db):
    cables = q.selAllCables(db)
    if cables:
        return {'status':True, 'cables':cables}
    else:
        return {'status':False, 'cables':{"upsieWoopsie"}}

def getCableNames(db):
    cables = q.selAllCablesNames(db)
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

##### POWER SOURCE #####
def getPSs(db):
    pss = q.selAllPowerSources(db)
    if pss:
        return {'status':True, 'pss':pss}
    else:
        return {'status':False, 'pss':{"upsieWoopsie"}}

def getPS(db, kwargs):
    ps = q.selPowerSource(db, kwargs)
    if ps:
        return {'status':True, 'ps':ps}
    else:
        return {'status':False, 'ps':{"upsieWoopsie"}}