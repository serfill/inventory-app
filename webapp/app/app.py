from flask import Flask, url_for, request, jsonify, render_template
from flask_moment import Moment
from pymongo import MongoClient
import datetime

import config
import webapi

api = webapi.webapi(config.MONGO_CONNECTION_STRING)

conn = MongoClient(config.MONGO_CONNECTION_STRING)
base = conn["inventory"]
coll = base["inventory"]
history = base["history"]

app = Flask(__name__)
moment = Moment(app)

@app.route("/")
def default():
    return "Ok"

@app.route("/api/v1/computers", methods=["POST", "GET"])
def api_v1_computers():
    if request.method == "POST":
        try:
            d = request.get_json()
            d["dt"] = datetime.datetime.now()
            coll.update_many(
                {"computername": d["computername"]},
                {"$set": d},
                upsert=True
            )
            history.insert_one({
                    "username": d["username"],
                    "computername": d["computername"],
                    "collect_date": d["collect_date"],
                    "dt": d["dt"]
                    })
            return("Add")
        except Exception as e:
            return(e)
    else: 
        try:
            return([i for i in coll.find({}, {'_id': False}).sort("computername", 1)])
        except Exception as e:
            return(e)

@app.route("/api/v1/history/<field>/<value>", methods=["GET"])
def api_v1_history_by(field, value):
    return api.getHistory(field,value)

@app.route("/api/v1/history", methods=["GET"])
def api_v1_history():
    return api.getHistory(None, None)


@app.route("/site/")
def site_index():
    return render_template("index.html", pc=coll.find().sort("computername", 1))

@app.route("/site/history/<field>/<value>")
def site_history_by(field, value):
    return render_template("history.html", rec=api.getHistory(field, value))

@app.route("/site/computer/<computername>")
def site_computer(computername):
    return render_template("info_pc.html", pc = api.getComputerInfo(computername))




if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=5000)