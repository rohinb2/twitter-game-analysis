from vaderSentiment.vaderSentiment import *
from twitter_auth import TwitterAuth
import tweepy

def get_tweets_containing_strings(api, query_strings, forbidden_string):
    NUM_OF_TWEETS_TO_QUERY = 2000 # max value is around 3,000 - 7 api calls per 100 tweets, 450 api calls.
    print("Searching for: ", NUM_OF_TWEETS_TO_QUERY, " tweets.")
    data = api.rate_limit_status()
    print("API Calls remaining: ", data['resources']['search']['/search/tweets']['remaining'])

    tweets = set()
    count = 0

    # can query by multiple strings
    for string in query_strings:
        for tweet in tweepy.Cursor(api.search, string).items(NUM_OF_TWEETS_TO_QUERY):
            count += 1
            #print("Tweets found: ", count)
            # if count % 100 == 0:
            #     data = api.rate_limit_status()
            #     print("Calls remaining: ", data['resources']['search']['/search/tweets']['remaining'])
            
            if forbidden_string in tweet.text:
                continue
            if tweet.retweet_count > 0:
                if tweet.text not in tweets:
                    tweets.add(tweet.text)
            else:
                tweets.add(tweet.text)
        
        print("Count of tweets found for ", query_strings[0], ": ", count)
    return tweets

def analyze_tweets_for_positive_feedback(api, query_strings, forbidden_string):
    analyzer = SentimentIntensityAnalyzer()
    positive_tweet_count = 0
    
    tweets = get_tweets_containing_strings(api, query_strings, forbidden_string)

    for tweet in tweets:
        if analyzer.polarity_scores(tweet)['pos'] > 0:
            positive_tweet_count += 1

    return positive_tweet_count

def get_twitter_supporter_percentages(home_team_city, home_team_name, away_team_city, away_team_name):
    try:
        api = tweepy.API(TwitterAuth.auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    except:
        print("Failed authentication")
    
    query_strings_home_team = ["#" + home_team_name] #, "#" + home_team_city + home_team_name]
    query_strings_away_team = ["#" + away_team_name] #, "#" + away_team_city + away_team_name]

    away_supporters_count = analyze_tweets_for_positive_feedback(api, query_strings_away_team, "#" + home_team_name)
    home_supporters_count = analyze_tweets_for_positive_feedback(api, query_strings_home_team, "#" + away_team_name)

    total = home_supporters_count + away_supporters_count
    d = { "percentage_supporting_away_team": (away_supporters_count / total), 
    "percentage_supporting_home_team": (home_supporters_count / total) }
    return d
