import os

from flask import Flask, request
from flask_pymongo import PyMongo
import numpy as np
from numpy.linalg import norm


# --------config-------- #
app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='dev',
    MONGO_URI=os.environ['MONGO_URI']
)

mongo = PyMongo(app)


@app.route('/nodes/all', methods=['GET'])
def fetch():
    # if needs to extract nodes from database
    nodes = {}
    return {'res': nodes}


@app.route('/upload', methods=['POST'])
def upload():
    uploaded_file = request.files['file']
    patient_file = uploaded_file.filename
    if uploaded_file.filename != '':
        uploaded_file.save('patient.npy')
    return {'res': 'patient trajectory uploaded.'}


@app.route('/search', methods=['POST', 'GET'])
def search():

    # parameter: date range, patients embedding, and entry to display
    params = request.json['searchTerms']

    # the params sent by frontend (str)
    startDate, endDate, entryReturn = params['startDate'], params['endDate'], int(
        params['entryToDisplay'])

    patient_data = np.load('patient.npy')

    # compute the distance between patient data and each user in the database
    embedding_collection = mongo.db.embeddings
    user_ids = embedding_collection.distinct('id', filter={}, session={})
    results = dict()
    for each_user in user_ids:
        docs = embedding_collection.find({'id': each_user}, sort=[('day', 1)])
        total_sim = 0
        for i, doc in enumerate(docs):
            embedding = np.fromstring(doc['embedding'][1:-1], sep=',')
            # compute each day similarity with patient data
            cos_sim = np.inner(
                patient_data[i], embedding)/(norm(patient_data[i]) * norm(embedding))
            print(cos_sim)
            # dist = np.norm(patient_data[i] - embedding)
            total_sim += cos_sim
        results[each_user] = total_sim

    # results: an ordered list of people(NRIC) and their similarity with the patient
    return {'res': sorted(results.items(), key=lambda item: item[1], reverse=True)[:entryReturn]}


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
