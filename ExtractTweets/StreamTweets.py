import re
import tweepy
from tweepy import OAuthHandler
import csv
import properties


class StreamListener(tweepy.StreamListener):
    def on_status(self, status):

        # Filter out retweets
        if status.retweeted or 'RT @' in status.text:
            return

        # Retain English tweets, ignore the rest
        if status.lang != "en":
            return

        text = status.text
        text = text.encode('utf-8')
        text = re.sub(r'(\w)\1{2,}', r'\1\1', text)
        textnopunct = re.sub(r"[^\w\d'-:~/$%?!'+@.#\s]+", '', text)

        description = status.user.description
        if description:
            description = re.sub(r"[^\w\d'-:~/$%?!'+@.#\s]+", '', description.encode('utf-8'))
        name = status.user.screen_name
        if name:
            name = name.encode('utf-8')
        followers = status.user.followers_count
        id_str = status.id_str
        if id_str:
            id_str = id_str.encode('utf-8')
        retweets = status.retweet_count
        hashtags = [word for word in text.split() if word[0] == "#"]
        print textnopunct
        csvFile = open(properties.input_file_path, 'a')
        csvWriter = csv.writer(csvFile)
        csvWriter.writerow([id_str, name, followers, description, textnopunct, retweets, hashtags])

    def on_error(self, status_code):
        if status_code == 420:
            return False


class TwitterClient(object):
    def __init__(self):

        try:
            self.auth = OAuthHandler(properties.consumer_key, properties.consumer_secret)
            self.auth.set_access_token(properties.access_token, properties.access_token_secret)
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")


def main():
    api = TwitterClient()
    stream_listener = StreamListener()
    stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
    stream.filter(track=properties.keywords)


if __name__ == "__main__":
    main()
