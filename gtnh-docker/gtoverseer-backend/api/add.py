import database.query as q
import sys

def addUser(db, username, email, password):
    status, err = q.insUser(db, {'username':username, 'email':email, 'password':password})
    if status:
        return True
    else:
        print(f"addUser: {err}", file=sys.stderr)
        return False
    