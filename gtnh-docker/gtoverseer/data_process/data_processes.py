import database.query as q
import sys, random ##########

def insRestart(db, data):
    # convert table tier to dictionary
    tiers = {row[2]: {"name": row[1], "ID": row[0]} for row in q.selTiers(db)}
    #first insert the station and get the ID
    if "computer_oc_address" in data[1]:
        q.insComputer(db, data[1])
    else:
        return False, "No valid controller / corrupted data"
    computer_oc_ID = q.selComputer(db, data[1]["computer_oc_address"])

    # now the machines

    for i in range(2,len(data)+1):

        data[i]["tier_ID"] = tiers[data[i]["input_eu"]]["ID"]
        data[i]["oc_computer_ID"] = computer_oc_ID
        
        try:
            q.insMachine(db, data[i])
            data[i]["machine_ID"] = q.selMachine(db, data[i]["oc_address"])
            q.insCoord(db, data[i])
        except Exception as e: # we keep this on the hush hush
            print(f"insRestart: Failed to insert machine {data[i]["name"]}: {e}", file=sys.stderr)
            continue
        
        if "is_power_source" in data[i]:
            q.insPowerSource(db, data[i])
       
    return True

def updWork(db, data):
    for i in range(1,len(data)+1):
        try:
            if (data[str(i)]["work_progress"] / data[str(i)]["work_progress_max"]) > 0.9:
                data[str(i)]["work_progress"] = 0
            q.updWork(db, data[str(i)])
        except Exception as e:
            print(f"updWork: Failed to update work: {e}", file=sys.stderr)
            continue
    return True
