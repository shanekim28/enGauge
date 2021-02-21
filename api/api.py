import nlpclient
import dbcontext
import json
import datetime
import string
import math
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config["DEBUG"] = True

dbcontext.init()

questions = []
answers = []


@app.route('/api/leaderboard', methods=['GET'])
def index():
    return jsonify(dbcontext.get_leaderboard())


# Adds a question or answer to the list
@app.route('/api/data', methods=['POST'])
def add_item():
    data = request.get_json()
    if (data.get('type') == 0):
        questions.append(data)

        # Reward user for asking/participating
        dbcontext.add_points(data.get('sender'), int(
            math.sqrt(len(data["content"]))))
    else:
        for answer in answers:
            # If the answer already exists
            if (answer["messageId"] == data["messageId"]):
                length_diff = len(data["reactedBy"]) - len(answer["reactedBy"])
                answer["reactedBy"] = data["reactedBy"]
                for reaction in range(length_diff):
                    dbcontext.add_points(answer["sender"], 25)

                return "200 OK"

        # Otherwise add the answer to the list
        answers.append(data)

        # Get referred question
        for question in questions:
            if (question["sender"] == data.get('sender')):
                continue

            if (question["messageId"] == data.get('refersTo')):
                questionTime = datetime.datetime.strptime(
                    question['sent-at'], f'%Y-%m-%d %H:%M:%S.%f')
        # If referring question exists
        if (questionTime):
            answerTime = datetime.datetime.strptime(
                data.get('sent-at'), f'%Y-%m-%d %H:%M:%S.%f')
            difference = answerTime - questionTime
            points = int(100 - (0.9 * difference.seconds /
                                60 * math.log(difference.seconds / 60))) \
                + int(2 * math.sqrt(len(data["content"])))
        else:
            points = 25

        if (points <= 0):
            points = 0

        dbcontext.add_points(data.get('sender'), points)
    return "200 OK"


# Check if sentence is question
@app.route('/api/index', methods=['GET'])
def get_pos():
    sentence = request.args.get('sentence')
    return jsonify({"value": nlpclient.process(sentence.lower())})

# Return all questions or answers


@ app.route('/api/data', methods=['GET'])
def get_data():
    if (request.args.get('type') == "questions"):
        return jsonify(questions)
    else:
        return jsonify(answers)


# Create user
@ app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()

    dbcontext.create_user(
        data['discordid'], data['firstname'], data['lastname'])
    return "204"


@app.route('/api/data/query', methods=['GET'])
def did_ask_question():
    for question in questions:
        if (question["sender"] == request.args.get('user')):
            return jsonify({"value": True, "messageId": question["messageId"]})

    return jsonify({"value": False})


app.run()
