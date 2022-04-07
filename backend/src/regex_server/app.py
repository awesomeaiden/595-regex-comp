from __future__ import absolute_import
from regex_server.database import database
from flask import Flask, request, Response
from flask_cors import CORS
import sys
import base64
from dotenv import load_dotenv
import json
from datetime import datetime
import uuid

load_dotenv()

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Connect to database
db = database.Database()


@app.route("/", methods=['GET'])
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/method1", methods=['POST'])
def generate_regex_visualization_method1():
    regex_str = request.args['str']
    base64arr = None
    with open("../test_img.png", 'rb') as f:
        byte_arr = f.read()
        base64arr = base64.standard_b64encode(byte_arr)
    return base64arr


@app.route("/log", methods=['POST'])
def log_data():
    print(request.json)
    datalog = request.json
    for payload in datalog["payloads"]:
        # If startup datapoint
        if payload["context"] == "startup":
            # First insert new participant
            new_participant = {
                "id": datalog["participantID"],
                "created": datalog["timestamp"]
            }
            db.insert_participant(new_participant)
            # Now insert startup datapoint
            payload["datapoint"]["created"] = datalog["timestamp"]
            db.insert_start(datalog["participantID"], payload["datapoint"])
        else:  # Assumed to be challenge datapoint
            payload["datapoint"]["created"] = datalog["timestamp"]
            payload["datapoint"]["context"] = payload["context"]
            db.insert_chal(datalog["participantID"], payload["datapoint"])
    return Response(status=200)


def main():
    if len(sys.argv) != 3:
        print("Error, usage: python app.py <ip> <port>")
        exit()

    ip = sys.argv[1]
    port = int(sys.argv[2])

    app.run(host=ip, port=port)


if __name__ == '__main__':
    main()
