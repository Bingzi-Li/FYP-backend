import os

from flask import Flask, request
#from flask_socketio import SocketIO
from flask_pymongo import PyMongo
import numpy as np


# --------config-------- #
app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='dev',
    MONGO_URI=os.environ['MONGO_URI']
)

mongo = PyMongo(app)

# if test_config is None:
#     # load the instance config, if it exists, when not testing
#     app.config.from_pyfile('config.py', silent=True)
# else:
#     # load the test config if passed in
#     app.config.from_mapping(test_config)

# # ensure the instance folder exists
# try:
#     os.makedirs(app.instance_path)
# except OSError:
#     pass
# socketio = SocketIO(app)

# a simple page that says hello


@app.route('/nodes/all', methods=['GET'])
def fetch():
    # TODO: extract nodes from database
    nodes = {}
    return {'res': nodes}


@app.route('/search', methods=['POST', 'GET'])
def search():

    # parameter: date range, patients embedding, and entry to display
    params = request.json

    # print the params sent by frontend
    print(params)

    # TODO: this is testing data, actually should get from frontend
    print(os.getcwd())
    patient_data = np.load('./test_data/converted.npy')
    display_num = 50  # number of entries to return

    # compute the distance between patient data and each user in the database
    embedding_collection = mongo.db.embeddings
    user_ids = embedding_collection.distinct('id', filter={}, session={})
    results = dict()
    for each_user in user_ids:
        docs = embedding_collection.find({'id': each_user}, sort=[('day', 1)])
        total_dist = 0
        for i, doc in enumerate(docs):
            embedding = np.fromstring(doc['embedding'][1:-1], sep=',')
            # compute each day similarity with patient data
            dist = np.linalg.norm(patient_data[i] - embedding)
            total_dist += dist
        results[each_user] = total_dist

    # results: an ordered list of people(NRIC) and their similarity with the patient
    return {'res': sorted(results.items(), key=lambda item: item[1])}


@app.route('/users/validate', methods=['POST'])
def validate():
    userinfo = request.json
    return {'res': 'Username and password received!'}


@app.route('/users/signout', methods=['POST'])
def signout():
    userinfo = request.json
    return {'res': 'User signed out!'}


@app.route('/embedding', methods=['POST'])
def embedding():
    data = request.json

    embedding_collection = mongo.db.embeddings

    embedding_collection.find_one_and_update(filter={'id': data['id'], 'day': data['day'] % 14}, update={
                                             '$set': {'day': data['day'], 'embedding': data['embedding']}}, upsert=True)
    return {'res': 'Embedding ' + str(data['id']) + str(data['day'])+'saved to database!'}


# @socketio.on('my event')
# def handle_my_custom_event(json, methods=['GET', 'POST']):
#     print('received my event: ' + str(json))
#     socketio.emit('my response', json, callback=messageReceived)


# if __name__ == '__main__':
#     socketio.run(app, debug=True)
