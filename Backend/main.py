from gevent import monkey
monkey.patch_all()


from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy

import logging
import json

import os 
from dotenv import load_dotenv, find_dotenv

env_path = find_dotenv()
if not env_path:    
    candidate = os.path.join(os.path.dirname(__file__), '..', 'Client', '.env')
    if os.path.exists(candidate):
        env_path = candidate
if env_path:
    load_dotenv(env_path)

database_url = os.getenv('DATABASE_URL')

#Extremely important commands

#& "C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres -p 4000
# cd C:/users/Sedri/Projects/SocialMedia/Client
# cd C:/users/Sedri/Projects/SocialMedia/Backend

#TRUNCATE TABLE message RESTART IDENTITY;
#db.session.add(Message(user = "Sedrik", text = "Hello from all the way in the database!"))
#db.session.commit()

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)



users = [
    {"name": "Sedrik",
     "Authorization": "Supreme_Leader",
     "Age": 84}]

Post = [
    {
        "user": "Sedrik",
        "text": "Hello, I'm looking for a partner to join me on my adventures. I'm a skilled warrior and a loyal companion. If you're interested, please reach out to me! #Adventurer #PartnerWanted"
        },
    {
        "user": "Sedrik",
        "text": "Send help! Andre keeps!"
        }
]
Posts = [{
        "user": "Sedrik",
        "text": "If your seeing this, this means very bad things"
}]

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='gevent')
socketio_app = app



app.config['SQLALCHEMY_DATABASE_URI'] = f"{database_url}"
db = SQLAlchemy(app)

#Database Modelling




class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(50), nullable=False)
    text = db.Column(db.String(500), nullable=False)
   
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(50), nullable=False)

def create_database():
    with app.app_context():
        db.create_all()
        db.session.add(User(userName = "Andre"))
        db.session.commit()

        

#Muh Database Routes


#RESTful Routes
@app.route('/api/message')
def get_message():
    return jsonify(message="Helo from Flask backend!")

@app.route('/api/button', methods=['POST'])
def recieve_input():
    data = request.get_json()
    return jsonify(status="success", data=data)


#SocketIO Routes
@socketio.on('get_data')
def retrieve_data(data):
   emit('submit_response', {'message': 'Hello using websockets!'})

@socketio.on('init_posts')
def handle_post():
    print("Initializing Posts")
    Posts = [{"user": message.user, "text": message.text}
    for message in Message.query.order_by(Message.id.desc()).all()]
    emit('post_response', json.dumps(Posts))

@socketio.on('new_post')
def new_post(data):

    print(data)
    db.session.add(Message(user = data["user"], text = data["text"]))
    db.session.commit()
    Posts = [{"user": message.user, "text": message.text}
    for message in Message.query.order_by(Message.id.desc()).all()]
    emit('Render_response', json.dumps(Posts), broadcast=True)

@app.route('/init-db')
def init_db():
    with app.app_context():
        db.create_all()
        db.session.add(User(userName="Andres"))
        db.session.commit()
    return "Database initialized!"



if __name__ == '__main__':
    import os
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        print("Loaded DB_PASSWORD:", os.getenv('DB_PASSWORD'))
        with app.app_context():
            print("Creating database...")
            create_database()


    
    socketio.run(app, port=5000, debug=True)

