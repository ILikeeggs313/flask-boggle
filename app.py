
from boggle import Boggle
from flask import Flask, jsonify, render_template, session, request
from flask_debugtoolbar import DebugToolbarExtension
app = Flask(__name__)
#debug toolbar set to True
app.debug = True
#secret key to enable flask session cookies
app.config['SECRET_KEY'] = '123456789'
toolbar = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

boggle_game = Boggle()

@app.route('/home-page')
def get_homepage():
    """SHOW THE BOARD."""
    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get('highscore', 0)
    nplays = session.get('nplays', 0)

    return render_template('index.html', board = board, highscore = highscore,
    nplays = nplays)

@app.route('/check-valid-word')
def check_word():
    """Check if the word is valid, or in dictionary."""
    word = request.args['word']
    board = session['board']
    resp = boggle_game.check_valid_word(board,word)

    return jsonify({'result':resp})

@app.route('/post-score', methods =['POST'])
def post_score():
    """Receive score, update num of plays, highscore"""
    score = request.json['score']
    highscore = session.get('highscore', 0)
    nplays = session.get('nplays', 0)
    session['nplays'] = nplays + 1
    session['highscore'] = max(score, highscore)

    return jsonify(brokeRecord = score > highscore)
