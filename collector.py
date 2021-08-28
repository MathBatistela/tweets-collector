
import tweepy
import time
from settings import *
import pika

# setting up RabbitMQ queue
connection = pika.BlockingConnection(pika.ConnectionParameters(HOST))
channel = connection.channel() 

# class for collecting real time tweet stream
class TweetListener(tweepy.StreamListener):

    # gets a tweet and send it to queue
    def on_status(self, status):
        channel.basic_publish(exchange='', routing_key=QUEUE, body=bytes(status.text, 'utf-8'))
        print(status.text)
            
        time.sleep(1)


if __name__ == "__main__":

    # setting up twitter api
    auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    print("-------------------------")
    print("\nSelect an option:\n")
    print("\t(0) Real time tweet stream")
    print("\t(1) Tweets from a specific date\n\n")

    # get user option
    option = input("Option > ")

    # declares the queue
    channel.queue_declare(queue=QUEUE)

    # collects real time tweets and filter them by location and topics
    if option == "0":
        listener = TweetListener()
        collector = tweepy.Stream(auth = api.auth, listener=listener)
        collector.filter(locations=TWEETS_LOCATIONS, track=TOPICS_LIST)

    # collects searched tweets since one date
    elif option == "1":
        date = input("Date (YYY-MM-DD): ")

        while True:
            # search tweets by date
            tweets = tweepy.Cursor(api.search,
                    q=TOPICS_LIST,
                    lang="pt-br",
                    since=date).items(100)

            for tweet in tweets:
                channel.basic_publish(exchange='', routing_key=QUEUE, body=tweet.text)

                print(tweet.text)
                time.sleep(1)

    else:
        print("Invalid option")