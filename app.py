from flask import Flask
from team_sentiment import *

app = Flask(__name__)

@app.route("/")
def hello():
    return str(get_twitter_supporter_percentages("Indianapolis", "Colts", "Baltimore", "Ravens"))

if __name__ == '__main__':
    app.run(debug=True)