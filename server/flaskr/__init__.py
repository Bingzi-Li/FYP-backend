import os

from flask import Flask, request
#from flask_socketio import SocketIO
from flask_pymongo import PyMongo


# --------config-------- #
app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
)

app.config["MONGO_URI"] = os.environ.get('MONGO_URI')
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


@app.route('/search', methods=['POST'])
def search():
    # TODO: extract nodes from database
    params = request.json
    results = None
    return {'res': results}


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
    id = request.args.get('id')
    trajectory = request.json
    embedding_collection = mongo.db.embeddings
    embedding_collection.insert({'id': id, 'data': trajectory})
    return {'res': f'Embedding {id} saved to database!'}


# @socketio.on('my event')
# def handle_my_custom_event(json, methods=['GET', 'POST']):
#     print('received my event: ' + str(json))
#     socketio.emit('my response', json, callback=messageReceived)


# if __name__ == '__main__':
#     socketio.run(app, debug=True)
