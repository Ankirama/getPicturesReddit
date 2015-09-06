#!/usr/bin/env python3
import praw, time, os, sqlite3, random, logging, sys, utilsReddit, tweepy
from urllib.request import urlopen
import urllib
from dropbox        import rest
import db
import dropboxHelper
import bot
import twitterHelper

class PicturesReddit():
    '''INFO'''
    NAME        = "getPicturesReddit"
    AUTHOR      = "Ankirama"
    VERSION     = 0.1
    DESCRIPTION = "Bot to download images from reddit with some variables"
    '''END INFO'''

    TIME_MIN = 300  # 60sec x 5 = 300
    TIME_MAX = 1800 # 60sec x 30 = 1800

    def __init__(self, reddit, dropbox, twitter):
        self.subreddit = reddit['subreddit']
        self.user_agent = reddit['user_agent']
        self.rootFolder = reddit['root']
        self.access_token = dropbox['token']
        self.rootDropbox = dropbox['root']
        self.submission = None

        logging.basicConfig(filename='./logs/redditBot.log', format='%(asctime)s %(funcName)s %(levelname)-15s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
        if not utilsReddit.createFolder(self.rootFolder):
            self.rootFolder = './'
        try:
            self.reddit = praw.Reddit(user_agent = self.user_agent)
            logging.info("Connected to reddit")
            self.mydb = db.Database('sqlite3.db')
            self.dropbox = dropboxHelper.DropboxHelper(self.access_token)
            self.twitter = twitterHelper.TwitterHelper(twitter['consumer_key'],
                                                       twitter['consumer_secret'],
                                                       twitter['access_key'],
                                                       twitter['access_secret'])
        except praw.errors.APIException as e:
            logging.error("Unable to use praw.Reddit (server side): %s", e)
            logging.info("========Bot stopped===========")
            raise praw.errors.APIException
        except praw.errors.ClientException as e:
            logging.error("Unable to use praw.Reddit (client side): %s", e)
            logging.info("========Bot stopped===========")
            raise praw.errors.ClientException
        except sqlite3.OperationalError:
            logging.info("========Bot stopped===========")
            raise sqlite3.OperationalError
        except tweepy.error.TweepError:
            logging.info("========Bot stopped===========")
            raise rest.ErrorResponse            
        except rest.ErrorResponse:
            logging.info("========Bot stopped===========")
            raise rest.ErrorResponse

    def __del__(self):
        del self.mydb

    def getPictureURL(self):
        self.submission = self.reddit.get_random_submission(self.subreddit)
        while (self.submission.url[len(self.submission.url) - 4 :] != '.jpg' and
               self.submission.url[len(self.submission.url) - 4 :] != '.png'): #and
#           re.search("(?<=http:\/\/)(i.imgur.com\/)\w+", submission.url)):
            logging.warning("[%s]: This is not a picture", self.submission.title)
            self.submission = self.reddit.get_random_submission(self.subreddit)
        logging.info("Picture random found from %s: title: %s | url: %s",
                     self.subreddit, self.submission.title, self.submission.url)
    
    def downloadImageFromURL(self, filename, pictureURL, folder):
        try:
            img = urlopen(pictureURL)
            logging.info("[%s] opened with urlopen", pictureURL)
        except urllib.error.HTTPError as e:
            logging.error("[%s]: unable to open this url with urlopen: %s", pictureURL, e)
        else:
            try:
                fileImg = open(folder + filename, 'wb')
                fileImg.write(img.read())
                fileImg.close()
                logging.info("[%s] saved into [%s]", filename, folder)
            except BaseException as e:
                logging.error("[%s] unable to save the file: %s", filename, e)

    def execute(self):
        while True:
            logging.info("Start to search new image")
            self.getPictureURL()
            picture = {'name': self.submission.title,
                       'url': self.submission.url,
                       'filename': self.submission.url[self.submission.url.rfind('/') + 1 :],
                       'anime': utilsReddit.extractAnimeName(self.submission.title)}
            try:
                nbEntriesPic = self.mydb.checkEntryPictures(picture['url'])
                if nbEntriesPic > 0:
                    continue
            except sqlite3.OperationalError:
                continue
            folder = self.rootFolder + picture['anime'] + '/' if picture['anime'] else self.rootFolder
            if self.mydb.addEntry(picture['name'], picture['filename'], picture['url'], folder):
                utilsReddit.createFolder(folder)
            self.downloadImageFromURL(picture['filename'], picture['url'], folder)
            self.twitter.updateMediaTweet(folder + picture['filename'], '[NSFW bot] ' + picture['name'])
            timeToWait = random.randint(self.TIME_MIN, self.TIME_MAX)
            logging.info("time until next picture: %d", timeToWait)
            time.sleep(timeToWait)

def main():
    try:
        getPictures = PicturesReddit(bot.getReddit(PicturesReddit.VERSION),
                                     bot.getDropbox(),
                                     bot.getTwitter())
        getPictures.execute()
    except BaseException as e:
        print("error: ", e)

if __name__ == "__main__":
    main()
