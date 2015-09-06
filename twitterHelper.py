import tweepy, logging

class TwitterHelper():
    def __init__(self, consumer_key, consumer_secret,
                 access_key, access_secret):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_key, access_secret)
        self.api = tweepy.API(auth)

        try:
            self.api.me()
        except tweepy.error.TweepError as e:
            logging.error("Unable to log into your twitter account: %s", e)
            raise tweepy.error.TweepError

    def updateMediaTweet(self, filename, status):
        try:
            self.api.update_with_media(filename, status)
            logging.info("[%s] updated on your twitter with status: %s", filename, status)
            return True
        except tweepy.error.TweepError as e:
            logging.error("Unable to update [%s] on twitter: %s", filename, e)
            return False

    def updateTweet(self, status):
        try:
            self.api.update_status(status)
            logging.info("Status updated on your twitter: %s", status)
            return True
        except tweepy.error.TweepError as e:
            logging.error("Unable to update status [%s] on twitter: %s", status, e)
            return False
