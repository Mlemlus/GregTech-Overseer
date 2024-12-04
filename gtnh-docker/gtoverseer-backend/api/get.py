import database.query as q
import sys ################

def loginProcess(db, email, password):
    nickname = q.selUserEmailPassword(db, {"email": str(email), "password": str(password)})[0]
    print(f"hey {nickname}", file=sys.stderr) #####################
    # priviliges and stuff can be returned from here
    #   *futureproofing*
    if nickname:
        return {'status':True, 'nickname':nickname}
    else:
        return {'status':False, 'nickname':""}
    