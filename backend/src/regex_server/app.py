from __future__ import absolute_import
from regex_server.database import database
from flask import Flask, request, Response
from flask_cors import CORS
import sys
import base64
from dotenv import load_dotenv
import subprocess
import copy
import json
from datetime import datetime
import uuid
from git import Repo

load_dotenv()

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Connect to GitHub Repo
my_repo = Repo('../../595-regex-comp/')

# Connect to database
db = database.Database()

STRING_QUESTIONS = ["stringA", "stringB", "stringC", "stringD"]
CREATE_QUESTIONS = ["createE", "createF", "createG", "createH"]
UPDATE_QUESTIONS = ["updateI", "updateJ", "updateK", "updateL"]

CONTEXT_QUESTIONS = {
    "control1": STRING_QUESTIONS,
    "control2": CREATE_QUESTIONS,
    "control3": UPDATE_QUESTIONS,
    "explain1": STRING_QUESTIONS,
    "explain2": CREATE_QUESTIONS,
    "explain3": UPDATE_QUESTIONS,
    "automata1": STRING_QUESTIONS,
    "automata2": CREATE_QUESTIONS,
    "automata3": UPDATE_QUESTIONS,
    "grex1": STRING_QUESTIONS,
    "grex2": CREATE_QUESTIONS,
    "grex3": UPDATE_QUESTIONS
}


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
    datalog = request.json
    print(datalog)
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

@app.route("/backup", methods=['POST'])
def backup_data():
    print("Backing up database.")
    db.backup();

    commit_message = 'Backup of database files'
    my_repo.index.add('backend/backups/')
    my_repo.index.commit(commit_message)
    origin = my_repo.remote('origin')
    origin.push()

    return Response(status=200)

def get_nth_key(dictionary, n=0):
    if n < 0:
        n += len(dictionary)
    for i, key in enumerate(dictionary.keys()):
        if i == n:
            return key
    raise IndexError("dictionary index out of range")


def get_first_key(dictionary):
    for key in dictionary:
        return key
    raise IndexError


@app.route("/sequence", methods=["GET"])
def get_sequence():
    # Initialize empty distribution
    distribution = copy.deepcopy(CONTEXT_QUESTIONS)
    for context in distribution:
        context_dict = dict()
        for question in distribution[context]:
            context_dict[question] = 0
        distribution[context] = context_dict

    # Get current counts of questions and place into dictionary
    question_counts = db.get_question_counts()
    for entry in question_counts:
        distribution[entry[0]][entry[1]] = entry[2]

    # sequence = [[control1 string question index, explain1 ..., automata1 ..., grex1 ...],
    #             [control2 create question index, explain2 ..., automata2 ..., grex2 ...],
    #             [control3 update question index, explain3 ..., automata3 ..., grex3 ...]]
    sequence = [[], [], []]
    # Now select the question with the least uses for each context
    sequence_ind = 0
    for context in distribution:
        # Which question has the lowest count for this context?
        low_question = get_first_key(distribution[context])
        low_count = distribution[context][low_question]
        for question in distribution[context]:
            if distribution[context][question] < low_count:
                low_question = question
                low_count = distribution[context][question]
        sequence[sequence_ind % 3].append(CONTEXT_QUESTIONS[context].index(low_question))

        # remove this question from consideration for rest of contexts that may use it
        i = sequence_ind + 3
        while i < len(distribution):
            dist_key = get_nth_key(distribution, i)
            distribution[dist_key].pop(low_question, None)
            i += 3

        sequence_ind += 1

    print("Optimal balancing sequence: " + str(sequence))

    return {
        "sequence": sequence
    }


@app.route("/grex", methods=["POST"])
def grex():
    # Get user inputted strings
    strings = request.json["strings"]
    grex_input = ["./grex"] + strings

    try:
        grex_output = subprocess.check_output(grex_input)
    except subprocess.CalledProcessError as e:
        print(e.output)
        return e.output

    grex_output = grex_output.decode("utf-8").rstrip()

    print(grex_output)
    return {
        "grex": grex_output
    }


def main():
    if len(sys.argv) != 3:
        print("Error, usage: python app.py <ip> <port>")
        exit()

    ip = sys.argv[1]
    port = int(sys.argv[2])

    app.run(host=ip, port=port)


if __name__ == '__main__':
    main()
