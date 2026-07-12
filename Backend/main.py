import eventlet
# Monkey-patch the stdlib before importing Flask/werkzeug and other libraries
eventlet.monkey_patch()

#socketIO dependencies
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit

#Python Classes
from Game import Game
from RunnerLoop import RunnerLoop


games = {}


app = Flask(__name__)
CORS(app)

socketio = SocketIO(app, cors_allowed_origins="*", async_mode ="eventlet")
socketio_app = app

#SocketIO Routes
@socketio.on('connect')
def handle_connect():
    sid = request.sid
    print(f"CONNECT: sid={sid}, existing sessions={len(games)}")
    print(f'Client connected: {sid}')

    game = Game()
    runner = RunnerLoop(game, tick_hz=60, on_state=lambda state: socketio.emit('position_update', state, room=sid))
    games[sid] = {'game': game, 'runner': runner}

    runner.start()
       
@socketio.on('disconnect')
def handle_disconnect():
    sid = request.sid
    print(f'Client disconnected: {sid}')
    if sid in games:
        entry = games[sid]
        runner = entry.get('runner')
        if runner:
            runner.stop()
        del games[sid]

@socketio.on('init')
def handle_init(data):
    sid = request.sid
    emit('init_response', {'message': 'Initialization complete', 'position': 150}, room=sid)
    

 

if __name__ == '__main__':
    
    socketio.run(app, port=5000, debug=False, use_reloader=False)

