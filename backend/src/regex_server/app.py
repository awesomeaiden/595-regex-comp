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
    "code1": STRING_QUESTIONS,
    "code2": CREATE_QUESTIONS,
    "code3": UPDATE_QUESTIONS
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


@app.route("/sequence", methods=["GET"])
def get_sequence():
    # First get current distribution of questions
    unordered_distribution = db.get_question_distribution()
    # Reorder list
    distribution = []
    for entry in unordered_distribution:
        if entry[0][0:4] == "cont":
            distribution.append(entry)
    for entry in unordered_distribution:
        if entry[0][0:4] == "expl":
            distribution.append(entry)
    for entry in unordered_distribution:
        if entry[0][0:4] == "auto":
            distribution.append(entry)
    for entry in unordered_distribution:
        if entry[0][0:4] == "code":
            distribution.append(entry)
    # Organize into dictionary by context, then by question
    dist_dict = dict()
    for count in distribution:
        # Is context in dictionary yet?
        if not count[0] in dist_dict:
            dist_dict[count[0]] = {
                count[1]: count[2]
            }
        else:
            dist_dict[count[0]][count[1]] = count[2]
    # Now select the question missing / with the least uses for each context
    print(dist_dict)
    sequence = [[], [], []]
    for context in dist_dict:
        print(str(context) + ":")
        # Any possible questions missing?
        missing_questions = [question for question in CONTEXT_QUESTIONS[context] if question not in dist_dict[context].keys()]
        print("missing_questions: " + str(missing_questions))
        if len(missing_questions) > 0:
            repeat = True
            for question in missing_questions:
                print(sequence)
                if CONTEXT_QUESTIONS[context].index(question) not in sequence[int(context[-1]) - 1]:
                    sequence[int(context[-1]) - 1].append(CONTEXT_QUESTIONS[context].index(question))
                    print(sequence)
                    repeat = False
                    break
            # Can't avoid repeating a question for this problem at this point
            if repeat:
                missing_indices = [i for i in [0, 1, 2, 3] if i not in sequence[int(context[-1]) - 1]]
                sequence[int(context[-1]) - 1].append(missing_indices[0])
                print(sequence)
        else:
            # Otherwise, which question has the lowest count for this context?
            low_count = dist_dict[context][dist_dict[context].keys()[0]]
            low_question = dist_dict[context].keys()[0]
            for question in dist_dict[context]:
                if dist_dict[context][question] < low_count:
                    low_question = question
            sequence[int(context[-1]) - 1].append(CONTEXT_QUESTIONS[context].index(low_question))

    print(sequence)

    return {
        "sequence": sequence
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
