# twitter-game-analysis
Returns which team in a sports game has more Twitter supporters at the time, using the Twitter API and NLTK Vader social media sentiment analysis. Basic API setup is done with Flask and Heroku.

## API Use

API is live at twitter-game-analysis.herokuapp.com.
The following syntax can be used to make a GET request:
http://twitter-game-analysis.herokuapp.com/game/?awayteam={AWAY TEAM OF YOUR CHOICE}&hometeam={HOME TEAM OF YOUR CHOICE}
