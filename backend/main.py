from flask_mail import Mail
from website import create_app
from flask_cors import CORS

from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO, emit
from flask import Flask, jsonify, request
app = create_app()
socketio = SocketIO(app, cors_allowed_origins="http://localhost:5173")




@socketio.on('message')
def handle_message(message):
    print('Received message:', message)
    emit('response', {'data': 'Message received!'})

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'renzoofama@gmail.com'
app.config['MAIL_PASSWORD'] = 'fhxm zopa etlh lcmu'
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})
jwt = JWTManager(app)
mail = Mail(app)

if __name__ == '__main__':
    socketio.run(app, debug=True,host='0.0.0.0', port=9000)