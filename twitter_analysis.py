import tweepy
from textblob import TextBlob
import re
from tweepy import OAuthHandler

class TwitterCall():
	def __init__(self):

		consumer_key = "XXXXXXXXXX"
		consumer_secret = "XXXXXXXXXX"
		access_token = "XXXXXXXXXX"
		access_secret = "XXXXXXXXXX"

		try:
			self.auth = OAuthHandler(consumer_key, consumer_secret)
			self.auth.set_access_token(access_token, access_secret)
			self.api = tweepy.API(self.auth)

		except:
			print("Error: Authentication Failed!")

	def clean_tweet(self, tweet):
		
		return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/S+)"," ",tweet).split())

	def get_tweet_sentiment(self, tweet):
		
		analysis = TextBlob(self.clean_tweet(tweet))
		#analysis = TextBlob(tweet)
		if analysis.sentiment.polarity > 0:
			return 'positive'
		elif analysis.sentiment.polarity < 0:
			return 'negative'
		else:
			return 'neutral'

	def get_tweets(self, query, count = 10):
		
		tweets = []

		try:
			fetched_tweets = self.api.search(q = query, count = count)
			for tweet in fetched_tweets:
				parsed_tweet = {}
				parsed_tweet['text'] = tweet.text
				parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
				if tweet.retweet_count > 0:
					if parsed_tweet not in tweets:
						tweets.append(parsed_tweet)
				else:
					tweets.append(parsed_tweet)

			return tweets

		except tweepy.TweepError as e:
			print("TweepError : ",e)

def main():

	api = TwitterCall()
	query = input("Enter the key word to be searched...")
	
	tweets = api.get_tweets(query, count = 1000)

	ptweets = [tweet for tweet in tweets if tweet['sentiment'] == "positive"]
	ntweets = [tweet for tweet in tweets if tweet['sentiment'] == "negative"]
	neutweets = [tweet for tweet in tweets if tweet['sentiment'] == "neutral"]

	print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))
	#print("\nPositive Tweets are - ")
	#for t in ptweets[:20]:
	#	print("\n\n",t['text'])

	print("\nNegative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))
	#print("\n\nNegative Tweets are - ")
	#for t in ntweets[:20]:
	#	print("\n\n",t['text'])

	ph = open("pos.txt","w")
	nh = open("neg.txt","w")

	for t in ptweets:
		ph.write(t['text'] + "\n")

	for t in ntweets:
		nh.write(t['text'] + "\n")

	ph.close()
	nh.close()

if __name__ == "__main__":
	main()