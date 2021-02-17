from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import configparser
import csv
from textblob import TextBlob
import re
import spacy
import io


#----------------------------------
# Read credentials from cinfig file
#----------------------------------

config = configparser.ConfigParser()
filepath = '../../credentials/web_api/twitter_credentials.cfg'
config.read(filepath)

API_KEY = config.get('Twitter', 'API_KEY')
API_KEY_SECRET = config.get('Twitter', 'API_KEY_SECRET')
ACCESS_TOKEN = config.get('Twitter', 'ACCESS_TOKEN')
ACCESS_TOKEN_SECRET =  config.get('Twitter', 'ACCESS_TOKEN_SECRET')

#----------------------------------
# Class
#----------------------------------

class TweetListener(StreamListener):
	def on_status(self, tweet):

		# Clean tweet.text 
		tweet_string = clean_tweet(tweet.text)

		print("@{} -------- {}".format(tweet.user.screen_name, tweet_string))

		with open('stream_data.csv', 'a', encoding="utf-8") as csv_file:
			csv_writer = csv.DictWriter(csv_file, fieldnames=['created_at', 'user_name','tweet', 'sentiment', 'subjectivity'], 
				lineterminator = '\n')

			blob = TextBlob(tweet_string).sentiment

			data = {
			    "created_at": tweet.created_at,
				"user_name": tweet.user.screen_name,
			    "tweet": tweet_string,
			     'sentiment': blob[0], 
			     'subjectivity': blob[1]
			    }

			csv_writer.writerow(data)

		return True

	def on_error(self,status):
		print(f"ERROR - status: {status}")

#----------------------------------
# Functions
#----------------------------------

def create_stream():
	'''
	Creates a tweet stream listener
	'''

	# Creating the authentication object
	auth = OAuthHandler(API_KEY, API_KEY_SECRET)
	# Setting your access token and secret
	auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

	listener = TweetListener()
	return Stream(auth, listener)	

def clean_tweet(tweet_string):
	tweet_string = deEmojify(tweet_string)
	tweet_string = re.sub('(@[A-Za-z0-9_]+)', '', tweet_string)
	tweet_string = re.sub('(http[A-Za-z0-9]+)', '', tweet_string)
	tweet_string = re.sub('RT', '', tweet_string)
	tweet_string = re.sub('[^\w\s]', '', tweet_string)

	return tweet_string

def deEmojify(inputString):
    return inputString.encode(encoding='ascii', errors='ignore').decode('ascii')

#----------------------------------
# Main
#----------------------------------

if __name__ == '__main__':

	with open('stream_data.csv', 'w', encoding='utf-8') as csv_file:
	    csv_writer = csv.DictWriter(csv_file, fieldnames=['created_at', 'user_name', 'tweet', 'sentiment', 'subjectivity'])
	    csv_writer.writeheader()

	stream = create_stream()
	stream.filter(track=['Mardi Gras'], languages=['en'])
	
