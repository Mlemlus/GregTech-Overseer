from flask import Flask, g
from routes.api import api_bp, initAddAdmin
from routes.data import data_bp
import os, time, shared, requests

# init Flask
app = Flask(__name__)
app.register_blueprint(api_bp)
app.register_blueprint(data_bp)

# init shared vals
shared.oc_stations = {}
shared.oc_stations_update_rate = int(os.getenv("UPDATE_RATE"))
shared.oc_stations_reinitialization_rate = int(os.getenv("REINITIALIZATION_RATE"))

@app.before_request
def before_request(): # executes before every request
    g.conn_params = { # flask global variable
        "dbname": os.getenv("DBNAME"),
        "user": os.getenv("USER"),
        "password": os.getenv("PASSWORD"),
        "host": os.getenv("HOST"),
        "port": os.getenv("PORT"),
    }

if __name__ == '__main__':
    # if we add the admin account every time, it has to exist (it gets updated on conflict)
    while "pigs can fly":
        status, err = initAddAdmin(
            {
                "dbname": os.getenv("DBNAME"),
                "user": os.getenv("USER"),
                "password": os.getenv("PASSWORD"),
                "host": os.getenv("HOST"),
                "port": os.getenv("PORT"),
            },
            {
                "username":os.getenv("ADMIN_USERNAME"),
                "email":os.getenv("ADMIN_EMAIL"),
                "password":os.getenv("ADMIN_PASSWORD"),
                "privileges":["Administrator"]
            })
        if status:
            break
        else:
            requests.post("http://10.21.31.5:40649/log",json={
                "text":f"api.initAddAdmin: no database connection: {err}"
            })
            time.sleep(5) # wait for DB to initialize 
    app.run(debug=False, host='0.0.0.0', port=40649)