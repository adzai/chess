from flask import Flask, request
from ai import Ai

app = Flask(__name__)

@app.route('/get-move')
def get_move():
    fen_str = request.args.get('fen')
    print(fen_str)
    if fen_str is None: 
        return "Provide fen"
    ai = Ai()
    value, move = ai.get_move(fen_str=fen_str)
    return move

if __name__ == '__main__':
    app.run(debug=True, port=5000)
