from vaderSentiment.vaderSentiment import *
from twitter_auth import TwitterAuth
import tweepy

def get_tweets_containing_strings(query_strings, forbidden_string):
    try:
        api = tweepy.API(TwitterAuth.auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    except:
        print("Failed authentication")
    tweets = set()

    for string in query_strings:
        count = 0
        try:
            for tweet in tweepy.Cursor(api.search, string).items(7000):
                count += 1
                if forbidden_string in tweet.text:
                    continue
                if tweet.retweet_count > 0:
                    if tweet.text not in tweets:
                        tweets.add(tweet.text)
                else:
                    tweets.add(tweet.text)
        except:
            print("Rate limit exceeded")
        print("Count of tweets found: ", count)
    return tweets

def analyze_tweets_for_positive_feedback(query_strings, forbidden_string):
    analyzer = SentimentIntensityAnalyzer()
    positive_tweet_count = 0
    
    tweets = get_tweets_containing_strings(query_strings, forbidden_string)

    for tweet in tweets:
        if analyzer.polarity_scores(tweet)['pos'] > 0:
            positive_tweet_count += 1

    return positive_tweet_count

def get_twitter_supporter_percentages(home_team_city, home_team_name, away_team_city, away_team_name):
    query_strings_home_team = ["#" + home_team_name] #, "#" + home_team_city + home_team_name]
    query_strings_away_team = ["#" + away_team_name] #, "#" + away_team_city + away_team_name]

    home_supporters_count = analyze_tweets_for_positive_feedback(query_strings_home_team, "#" + away_team_name)
    away_supporters_count = analyze_tweets_for_positive_feedback(query_strings_away_team, "#" + home_team_name)
    total = home_supporters_count + away_supporters_count
    return [home_supporters_count / total, away_supporters_count / total]

