import database.query as q
import sys ################

##### USER #####
def loginProcess(db, data):
    status, username = q.selUserEmailPassword(db, data)
    return {"status":status, "username":username}

def getUsers(db):
    status, users = q.selAllUsers(db)
    return {"status":status, "users":users}

    
def getUser(db, username):
    status, user = q.selUserUsername(db, username)
    return {"status":status, "user":user}

##### MACHINE #####
def getMachines(db):
    status, machines = q.machineReport(db)
    return {"status":status, "machines":machines}

def searchMachines(db, kwargs):
    kwargs["wild_search"] = "%" + kwargs["search"] + "%" # prep the search
    status, machines = q.selSearchMachines(db, kwargs)
    return {"status":status, "machines":machines}

##### POWER NETWORK #####
def getPowerNetworkNames(db):
    status, pnnames = q.selAllNetowrksNames(db)
    return {"status":status, "pnnames":pnnames}

def getPNs(db):
    status, pns = q.selAllPowerNetworks(db)
    return {"status":status, "pns":pns}

##### CABLE #####
def getCables(db):
    status, cables = q.selAllCables(db)
    return {"status":status, "cables":cables}

def getCableNames(db):
    status, cables = q.selAllCablesNames(db)
    return {"status":status, "cables":cables}

##### TIER #####
def getTierNames(db):
    status, tiers = q.selAllTierNames(db)
    return {"status":status, "tiers":tiers}

##### POWER SOURCE #####
def getPSs(db):
    status, pss = q.selAllPowerSources(db)
    return {"status":status, "pss":pss}

def getPS(db, kwargs):
    status, ps = q.selPowerSource(db, kwargs)
    return {"status":status, "ps":ps}