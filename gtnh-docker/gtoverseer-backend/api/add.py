import database.query as q
import sys

def addUser(db, username, email, password):
    status, err = q.insUser(db, {"username":username, "email":email, "password":password})
    if status:
        return True
    else:
        print(f"addUser: {err}", file=sys.stderr)
        return False

def addCable(db, name, density, tier_name, max_amp, loss):
    status, err = q.insCable(
        db, 
        {
            "name":name,
            "density":density,
            "tier_name":tier_name,
            "max_amp":max_amp,
            "loss":loss
        })
    if status:
        return {'status':True}
    else:
        print(f"addUser: {err}", file=sys.stderr)
        return {'status':False}