import importlib
import json

import flask
from flask import render_template, request, send_from_directory, redirect
from jinja2 import Markup

import baroque_chess_server
import game_to_svg

app = flask.Flask(__name__)

# victories is a map from player names to the number of victories.
victories = {'TURN_LIMIT': 0, 'DRAW': 0}
# current_game is a continuation representing the game progress.
current_game = None
# player_list is a list of player module names.
player_list = []
current_player1 = None
current_player2 = None
is_all_games = False
player_index1 = 0
player_index2 = 0

def initialize():
    with open('player_list.txt') as f:
        for line in f.readlines():
            l = line.strip()
            player_list.append(l)
            victories[l] = 0

@app.route('/')
def index():
    return render_template('base.html', player_list=player_list,
                results=list(sorted(victories.items(), key=lambda x: x[1], reverse=True)))

def init_game(p1, p2):
    global current_player1
    global current_player2
    current_player1 = p1
    current_player2 = p2
    player1 = importlib.import_module(p1)
    player2 = importlib.import_module(p2)
    baroque_chess_server.initialize(player1, player2,
            time_per_move=1.0, turn_limit=60)
    global current_game
    current_game = baroque_chess_server.runGame()

@app.route('/init', methods=['POST'])
def init():
    print('init game')
    p1 = request.form['player1']
    p2 = request.form['player2']
    init_game(p1, p2)
    return redirect('/first_turn')

@app.route('/first_turn')
def first_turn():
    results = next(current_game)
    if len(results) == 2:
        print('game failed')
        print(results)
        winner = results[1]
        if winner == 'BLACK':
            winner = current_player2
        elif winner == 'WHITE':
            winner = current_player1
        if winner in victories:
            victories[winner] += 1
        return render_template('error.html', message=results[0])
    elif len(results) == 3:
        game_svg = game_to_svg.game_to_svg(results[2])
        move_report = results[0]
        remark = results[1]
        return render_template('game.html',
                player1=current_player1,
                player2=current_player2,
                board=Markup(str(game_svg.to_str())),
                move_report=move_report,
                remark=remark,
                results=list(sorted(victories.items(), key=lambda x: x[1], reverse=True)))
    print(len(results))
    print('results:', results)
    return 'abc'

@app.route('/play_next_game')
def play_next_game():
    game_is_initialized = False
    while not game_is_initialized:
        global player_index1
        global player_index2
        if player_index2 == len(player_list) - 1 and player_index1 == len(player_list) - 1:
            return redirect('/')
        player_index2 += 1
        if player_index1 == player_index2:
            continue
        remainder = int(player_index2/len(player_list))
        player_index2 = player_index2 % len(player_list)
        player_index1 += remainder
        p1 = player_list[player_index1]
        p2 = player_list[player_index2]
        try:
            init_game(p1, p2)
            game_is_initialized = True
        except:
            print('ERROR: game failed to initialize.')
    return redirect('/first_turn')


@app.route('/game_update', methods=['POST'])
def game_update():
    print('game update')
    if current_game is None:
        return json.dumps({'result': 'none'})

    try:
        results = next(current_game)
    except Exception as e:
        print(e)
        return json.dumps({'result': 'done'})
    print(results)
    if len(results) == 2:
        winner = results[1]
        if winner == 'BLACK':
            winner = current_player2
        elif winner == 'WHITE':
            winner = current_player1
        print('game over: winner={0}'.format(winner))
        if winner in victories:
            victories[winner] += 1
        return json.dumps({'winner': winner})
    elif len(results) == 3:
        game_svg = game_to_svg.game_to_svg(results[2])
        move_report = results[0]
        remark = results[1]
        victory_results = list(sorted(victories.items(), key=lambda x: x[1], reverse=True))
        return json.dumps({
                'board': Markup(str(game_svg.to_str())),
                'remark': remark,
                'move_report': move_report,
                'player1': current_player1,
                'player2': current_player2,
                'results': victory_results,
                })

if __name__ == '__main__':
    initialize()
    app.run(debug=True)
