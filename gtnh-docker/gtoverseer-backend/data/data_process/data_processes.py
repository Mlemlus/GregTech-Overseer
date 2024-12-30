import data.database.query as q
import requests

def insRestart(db, data): # Handling of data for the OC reinitialization
    # convert table tier to dictionary
    _, raw_tiers = q.selTiers(db)
    tiers = {row[2]: {"name": row[1], "ID": row[0]} for row in raw_tiers}

    # first insert the OC Station and get it's database ID
    if "computer_oc_address" in data[1]:
        q.insComputer(db, data[1])
    else:
        return False ##### Rework error handling for OC stations # Update: I refuse
    status, computer_oc_ID = q.selComputer(db, data[1])
    if not status: # Failed to add OC station
        return False

    # now the machines
    for i in range(2,len(data)+1):
        data[i]["tier_ID"] = tiers[data[i]["input_eu"]]["ID"]
        data[i]["oc_computer_ID"] = computer_oc_ID
        try:
            q.insMachine(db, data[i])
            q.insCoord(db, data[i])
        except Exception as e: # we keep this on the hush hush
            requests.post("http://10.21.31.5:40649/log",json={
                "text":f"data_processes.insRestart: Failed to insert machine {data[i]["name"]}: {e}"
            })
            continue
        if "is_power_source" in data[i]:
            q.insPowerSource(db, data[i])
    return True #### Return something usefull like number of machines or just nothing # Update: I still refuse

def updWork(db, data): # The sauce, updates the database with work progress of the machines
    for i in range(1,len(data)+1):
        try:
            q.updWork(db, data[str(i)])
        except Exception as e:
            requests.post("http://10.21.31.5:40649/log",json={
                "text":f"data_processes.updWork: Failed to update work: {e}"
            })
            continue
    return True

def logStatus(db, kwargs):
    if "username" in kwargs:
        q.insLogUsername(db,kwargs)
    else:
        q.insLog(db,kwargs)
    return {"status":True}
