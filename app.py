from flask import Flask
from flask import jsonify
from flask import request
import os
from team_sentiment import *

app = Flask(__name__)
@app.route('/', methods=['GET'])
def blank_page():
    return "Use required syntax to get JSON game data. \n Example: http://twitter-game-analysis.herokuapp.com/game/?awayteam={AWAY TEAM OF YOUR CHOICE}&hometeam={HOME TEAM OF YOUR CHOICE}"

@app.route('/game/', methods=['GET'])
def game_tweets():

    away_team_city = request.args.get('awaycity', '')
    away_team_name = request.args.get('awayteam', 'Bears')
    home_team_city = request.args.get('homecity', '')
    home_team_name = request.args.get('hometeam', 'Packers')

    return jsonify(get_twitter_supporter_percentages(home_team_city, home_team_name, away_team_city, away_team_name))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)