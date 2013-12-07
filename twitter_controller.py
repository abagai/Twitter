__author__ = 'owner'
__faggot__ = 'venkat'

from Tkinter import *
from ttk import Frame, Style
import twitter_db_ops
from idlelib.WidgetRedirector import WidgetRedirector
import tkMessageBox
from PIL import ImageTk
import subprocess
import threading
import Queue
import os
from twitter_interface import *
from twitter_reader import *
from twitter_db_ops import *
from datetime import datetime

# The main class for this module. This class is the controller and defines the behaviours.
class SInterface():

    def __init__(self):
        # This is the model. The db class is a wrapper around database operations.
        self.dbops = TwitterDbOps("")
        self.root =Tk()
        self.root.geometry("1150x400+100+100")

        '''
        self.consumerKey = 'IFycAuEiZOo7mNOmNuW1lw'
        self.consumerSecret = 'E8MuIeoAKEWhLfbVDJAYyVL5sw9XIlEIbchqIotjxsE'
        self.accessKey = '35871247-89JyKTkbtn9L9V4fmkMMD7qHuOE39leWxJunutcSn'
        self.accessSecret = 'c6lxvaPOStYBWplXGZdW0AbhL00bMwVDReJflOc902fxg'
        '''
        self.consumerKey = 'jf1RuBnCqdQCNmLX0frLg'
        self.consumerSecret = 'ThqOiemmb6u0unxovHEg9r9m4Lf0MaI30nqh3gwedI'
        self.accessKey = '1106939719-KyTHxcGncJp0vgxTjH8P2AmaGQ13B5ert7YZR0t'
        self.accessSecret = 'PqIuAYKTuKFfrg24CAhuwigh5R2udkl2Fls06mTaZLhXZ'

        self.tweetReader = TwitterReader(self.consumerKey,self.consumerSecret,self.accessKey,self.accessSecret)

        self.view = View(self.root, self)
        self.root.protocol('WM_DELETE_WINDOW', self.close)
        self.root.mainloop()

    def close(self):
        self.root.destroy()

    def verifyUsername(self):
        self.valid = False
        if self.tweetReader.lookup_user(self.view.username.get()):
            self.view.username.config(bg='green')
            self.view.appendText("User: %s is valid!" %self.view.username.get())
            self.valid = True
        else:
            self.view.username.config(bg='red')

    def getTweets(self):
        try:
            if self.valid:
                try:
                    self.dbops.setup()
                    self.view.appendText("Get tweets and inputting into database...")
                    tweets=self.tweetReader.get_tweets_from_user(self.view.username.get(),int(self.view.numTweets.get()))
                    self.tweetsToDB(tweets)
                    #self.view.appendText(str(len(tweets)))
                    self.view.appendText("Done getting tweets!")
                except TwitterReaderException:
                    self.view.appendText("Rate Limit Exceeded; Please wait 15 minutes.")
        except AttributeError:
            self.view.appendText("Please enter and verify a user.")

    def listTweets(self):
        #print self.view.numTweets.get()
        if self.view.numTweets.get() == "":
            tweets = self.dbops.getTweets(self.view.numTweets.get(),False)
        else:
            tweets = self.dbops.getTweets(self.view.numTweets.get(),True)
        for tweet in tweets:
            self.view.appendText(tweet[2])
            self.view.appendText(tweet[1] + "\n")

    def mostHash(self):
        if self.view.numTweets.get() == "":
            hashes = self.dbops.getHashtags()
        else:
            hashes = self.getHastagsCount(self.view.numTweets.get())
        hashdict = {}
        hasharray = []

        for hash in hashes:
            if hash[0].lower() in hashdict:
                hashdict[hash[0].lower()]= hashdict[hash[0].lower()]+1
            else:
                hashdict[hash[0].lower()] = 1
        for n in hashdict:
            hasharray.append((hashdict[n],n))
        hasharray.sort(reverse=True)
        self.view.appendText("Most used Hashtags:")
        for n in hasharray:
            self.view.appendText('%s used %d times'%(n[1],n[0]))
        self.view.appendText('\n')

    def timeGraph(self):
        pass

    def communicated(self):
        refers = self.dbops.getReferences()
        refdict = {}
        refarray = []
        for refer in refers:
            if refer[0].lower() in refdict:
                refdict[refer[0].lower()]= refdict[refer[0].lower()]+1
            else:
                refdict[refer[0].lower()] = 1
        for n in refdict:
            refarray.append((refdict[n],n))
        refarray.sort(reverse=True)
        self.view.appendText("Most used References:")
        for n in refarray:
            self.view.appendText('%s used %d times'%(n[1],n[0]))
        self.view.appendText('\n')

    def tweetsToDB(self,tweets):
        tweet_count = 1
        for tweet in tweets:
            self.dbops.createTweet(tweet['text'], self.tweetReader.parse_date(tweet['created_at']))
            tweet_count+=1


    def getHastagsCount(self,count):
        tweets = self.dbops.getTweets(count,True)
        hashes = self.dbops.getHashtags()
        countedHashes = []

        for tweet in tweets:
            for hash in hashes:
                if tweet[0] == hash[1]:
                    countedHashes.append(hash)

    def date_filter(self, tweet_date, date1=datetime(1970,1,1), date2=datetime.now()):
        return date1 <  tweet_date < date2

    #call twitter stuff
