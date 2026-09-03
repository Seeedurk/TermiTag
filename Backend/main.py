import eventlet
# Monkey-patch the stdlib before importing Flask/werkzeug and other libraries
eventlet.monkey_patch()

#socketIO dependencies
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import os

#Python Classes
from Game import Game
from RunnerLoop import RunnerLoop


games = {}


app = Flask(__name__)
FRONTEND_ORIGIN = os.environ.get("FRONTEND_ORIGIN", "*")  
CORS(app, origins=FRONTEND_ORIGIN)

socketio = SocketIO(app, cors_allowed_origins="*", async_mode ="eventlet")
socketio_app = app

#SocketIO Routes
@socketio.on('connect')
def handle_connect():
    sid = request.sid
    print(f"CONNECT: sid={sid}, existing sessions={len(games)}")
    print(f'Client connected: {sid}')

    game = Game()
    runner = RunnerLoop(
        game,
        tick_hz=45,
        on_state=lambda state: socketio.emit(
            'position_update',
            state,
            room=sid
        )
    )
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
            try:
                runner.stop()
            except Exception:
                pass
        del games[sid]

@socketio.on('init')
def handle_init(data):
    sid = request.sid
    emit('init_response', {'message': 'Initialization complete', 'position': 150}, room=sid)
    if sid in games:
        emit('settings_response', games[sid]['game'].settings, room=sid)

@socketio.on('settings')
@socketio.on('settingsChange')
def handle_settings(data):
    sid = request.sid
    if sid not in games:
        return

    game = games[sid]['game']
    game.apply_settings(data)
    emit('settings_response', game.settings, room=sid)

@socketio.on('pause')
def handle_pause(data):
    sid = request.sid 
    if sid in games:
        selectedEntry = games[sid]
        selectedRunner = selectedEntry.get('runner')
        selectedRunner.paused = data
        selectedEntry.ended = False

@socketio.on('reset')
def handle_reset():
    sid = request.sid
    if sid in games:
        selectedEntry = games[sid]
        selectedGame = selectedEntry.get('game')
        selectedGame.gameReset()
        selectedGame.ended = False


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host="0.0.0.0", port=port, debug=False, use_reloader=False)

