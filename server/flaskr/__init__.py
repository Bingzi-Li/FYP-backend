import os

from flask import Flask, request
from flask_socketio import SocketIO


# --------config-------- #
app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
)

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


@app.route('/hello')
def hello():
    return {'res': 'Hello, World!'}


@app.route('/users/validate', methods=['POST'])
def validate():
    print(request.json)
    return {'res': 'Username and password received!'}


# @socketio.on('my event')
# def handle_my_custom_event(json, methods=['GET', 'POST']):
#     print('received my event: ' + str(json))
#     socketio.emit('my response', json, callback=messageReceived)


# if __name__ == '__main__':
#     socketio.run(app, debug=True)
