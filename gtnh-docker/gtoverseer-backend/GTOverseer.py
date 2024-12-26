from flask import Flask, g
from routes.api import api_bp, initAddAdmin
from routes.data import data_bp
import os, time, sys

app = Flask(__name__)
app.register_blueprint(api_bp)
app.register_blueprint(data_bp)

@app.before_request
def before_request(): # executes before every request
    g.conn_params = { # flask global variable
        "dbname": os.getenv("DBNAME"),
        "user": os.getenv("USER"),
        "password": os.getenv("PASSWORD"),
        "host": os.getenv("HOST"),
        "port": os.getenv("PORT")
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
                "port": os.getenv("PORT")
            },
            {
                "username":os.getenv("ADMIN_USERNAME"),
                "email":os.getenv("ADMIN_EMAIL"),
                "password":os.getenv("ADMIN_PASSWORD")
            })
        if status:
            break
        else:
            print(f"api.initAddAdmin: no database connection: {err}", file=sys.stderr)
            time.sleep(5) # wait for DB to initialize 
    app.run(debug=True, host='0.0.0.0', port=40649)