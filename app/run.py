import sys
import os
dir_name = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_name, '../'))

from game.tictactoe import TicTacToeState
from game.alpha_beta import AlphaBetaAgent

from flask import Flask, jsonify, render_template, request, send_from_directory, session
from app.utils import lock, release, lock_session

EMPTY_STR = ''


app = Flask(__name__, static_folder='./static', template_folder='./templates')
app.config.from_mapping(
    SECRET_KEY='yek-terces-esrever-a-si-siht'
)

@app.route('/')
def initialize():
    if not 'init' in session:
        session['init'] = True
        session['board'] = None
        session['turn'] = None
        session['wait'] = True
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/make-board', methods=['POST'])
def make_board():
    if not 'init' in session:
        return 'Session not initialized', 405
    
    request_body = request.get_json(force=True)
    size, turn = request_body['size'], request_body['turn']
    board = [[EMPTY_STR]*size]*size
    
    if turn == 'O':
        session['turn'] = 'X'
    elif turn == 'X':
        session['turn'] = 'O'
    else:
        return 'Invalid turn, expected either X or O', 400
    
    agent = AlphaBetaAgent()
    session['board'] = board
    
    if turn == 'X':
        session['wait'] = False
        return jsonify()
    else:
        lock(session)
        game_state = TicTacToeState(board, session['turn'])
        action = agent.search(game_state)
        session['board'] = game_state.getNextState(action).getBoard()
        release(session)
        return jsonify(x=action[0], y=action[1])

@app.route('/make-move', methods=['POST'])
@lock_session(session)
def make_move():
    request_body = request.get_json(force=True)
    x, y = request_body['x'], request_body['y']
    
    game_state = TicTacToeState(session['board'], session['turn'])
    game_state = game_state.getNextState((x,y))
    session['board'] = game_state.getBoard()
    if game_state.isGameOver():
        winner = game_state.getWinner()
        return jsonify(over=True, winner=winner)
    
    agent = AlphaBetaAgent()
    action = agent.search(game_state)
    game_state = game_state.getNextState(action)
    session['board'] = game_state.getBoard()
    if game_state.isGameOver():
        winner = game_state.getWinner()
        return jsonify(over=True, winner=winner, x=action[0], y=action[1])
    else:
        return jsonify(over=False, x=action[0], y=action[1])


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
