from flask import Flask
from flask import jsonify
from flask import request
from team_sentiment import *

app = Flask(__name__)

@app.route('/game/', methods=['GET'])
def game_tweets():

    away_team_city = request.args.get('awaycity', '')
    away_team_name = request.args.get('awayteam')
    home_team_city = request.args.get('homecity', '')
    home_team_name = request.args.get('hometeam')

    return jsonify(get_twitter_supporter_percentages(home_team_city, home_team_name, away_team_city, away_team_name))

if __name__ == '__main__':
    app.run(debug=True)