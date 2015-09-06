# getPicturesReddit
bot to download automatically pictures / images from reddit

# before to start
lib used: praw (https://github.com/praw-dev/praw)
api rules: https://github.com/reddit/reddit/wiki/API#rules

Current "bugs":
  directory created before to download image -> if image fails the directory could be present but empty will be useless: change it
  change current download / directory to a os.rename (to move root image into right folder)

  Use a class to keep trace for FOLDER_TO_SAVE after init update

  Need to add image without extension


# Twitter
lib used: https://github.com/tweepy/tweepy
doc : http://tweepy.readthedocs.org/en/v3.4.0/

to get your access / consumer keys/secret -> https://apps.twitter.com/
