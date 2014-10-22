#!/usr/bin/env python
# -*- coding:utf-8 -*-

import tweepy_basic
import rtlib
import sys
import datetime,os

def log_check(datestr,log_file_name,limit_minutes=None):
    f = open("log/"+log_file_name,"r")
    datelist = []
    if limit_minutes == None:
        for line in f:
            datelist.append(line.strip())
        if datestr in datelist:
            return True
        else:
            return False
    else:
        for line in f:
            datelist.append(line.strip().split(","))
        if [datestr,str(limit_minutes)] in datelist:
            return True
        else:
            return False

class twitime_logger:
    def __init__(self):
        rt = rtlib.rescuetime()
        twitter_client = ["Twitter","Twitter for Android","TweetDeck"]
        self.api = tweepy_basic.setup_ariapp()
        self.today_twitime = rt.gettime(twitter_client)

        self.client_today_twitime = dict()
        for client in twitter_client:
            try:
                self.client_today_twitime[client] = rt.gettime([client])
            except:
                self.client_today_twitime[cient] = 0

        self.today = datetime.datetime.today().strftime("%Y%m%d")

    def today_spent_time(self):
        tweet = "@arieee0 今日あなたはtwitterに{:.1f}分費やしています…"\
                "無駄に時間を使っていますね…".format(float(self.today_twitime)/60)
        #self.api.update_status(tweet)
        print "Made tweet:{}".format(tweet)

    def overtime(self,limit_minutes):
        c_time = datetime.datetime.today().strftime("%H:%M")
        if not log_check(self.today,"overtime",limit_minutes):
            if self.today_twitime > limit_minutes * 60:
                tweet = "@arieee0 本日のtwitter累計時間が{}分を超えました…"\
                        "大丈夫ですか…".format(limit_minutes)
                #self.api.update_status(tweet)
                print "{} Made tweet:{}".format(c_time,tweet)
                logf = open("log/overtime","a+")
                logf.write(self.today+","+str(limit_minutes)+"\n")
                logf.close()
            else:
                #print "twitterに費やした時間が{}分を超えなかったのでツイートされませんでした {}".format(limit_minutes,c_time)
                pass

    def daily_summary(self):
        limit_sec = 60 * 60
        if self.today_twitime > limit_sec or True: #必ずtweetするように変更
            c = self.client_today_twitime
            al = self.today_twitime
            #tweet = "@arieee0 今日あなたはtwitterに{:.1f}分費やしました…\n"\
            #        "内訳 Web:{:.1f}%,TweetDeck:{:.1f}%,Android:{:.1f}%\n"\
            #        "無駄な時間を過ごしましたね…".format(self.today_twitime/float(60),100*float(c["Twitter"])/al,100*float(c["TweetDeck"])/al,100*float(c["Twitter for Android"])/al)
            #self.api.update_status(tweet)
            tweet = "@arieee0 今日あなたはtwitterに{:.1f}分費やしました…\n".format(self.today_twitime/float(60))
            self.api.update_with_media(filename="../Mydata/picgraph/tweet_graph.png",status=tweet)
            print "Made tweet:{}".format(tweet)
        else:
            print "本日({})twitterに費やした時間は{}分です\n{}分を超えなかったのでツイートされませんでした".format(self.today_twitime/float(60),self.today,limit_sec/60)
            

if __name__ == "__main__":
    os.chdir("/home/ysuzuki/MyApplication/rescueapp")

    cmd = sys.argv[1]
    tlog = twitime_logger()
    if cmd == "today":
        tlog.today_spent_time()
    elif cmd == "overtime":
        limit_time = int(sys.argv[2])
        tlog.overtime(limit_time)
    elif cmd == "summary":
        tlog.daily_summary()
