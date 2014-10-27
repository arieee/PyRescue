#!/usr/bin/env python
# -*- coding:utf-8 -*-

from rescuetime.api.service import Service
from rescuetime.api.access import AnalyticApiKey
# official API documentation is here https://www.rescuetime.com/anapi/setup/documentation
import datetime,sys,os
from pprint import PrettyPrinter
from collections import defaultdict

def test():
    print "RescueTime class TEST"
    rt = RescueTime(beginDay="20141015",endDay="20141019")
    pp = PrettyPrinter()
    print "confirm what raw data are"
    pp.pprint(rt.jsonRawData)
    print "getAllData"
    
    rt.getAllData([["Twitter","Twitter for Android"],["Hulu"]],["2","-1"],["General Software Development"])


class Activity:
    def __init__(self,data):
        self.date = data[0]
        self.timespent = int(data[1])
        self.num_of_people = int(data[2])
        self.activity = data[3]
        self.category = data[4]
        self.productivity = str(data[5]) #-2,-1,0,1,2
 
class RescueJSONParser:
    def __init__(self,fetch_data):
        self.activityDic = defaultdict(lambda:defaultdict(float))
        self.productivityDic = defaultdict(lambda:defaultdict(float))
        self.categoryDic = defaultdict(lambda:defaultdict(float))

        for act in fetch_data['rows']:
            a = Activity(act)
            date = datetime.datetime.strptime(a.date[0:10],"%Y-%m-%d").strftime("%Y%m%d")

            self.activityDic[date][a.activity] += a.timespent
            self.productivityDic[date][a.productivity] += a.timespent
            self.categoryDic[date][a.category] += a.timespent

    def activityTime(self,date,activityName):
        if date in self.activityDic and activityName in self.activityDic[date]:
            return self.activityDic[date][activityName]
        else:
            return 0.0

    def productivityTime(self,date,productivityNumber):
        if date in self.productivityDic and productivityNumber in self.productivityDic[date]:
            return self.productivityDic[date][productivityNumber]
        else:
            return 0.0

    def categoryTime(self,date,categoryName):
        if date in self.categoryDic and categoryName in self.categoryDic[date]:
            return self.categoryDic[date][categoryName]
        else:
            return 0.0

    def fetchAllData(self,dateList,activityGroupList,productivityList,categoryGroupList):
        for date in dateList:
            output = []
            for activityGroup in activityGroupList:
                sec = 0
                for activity in activityGroup:
                    sec += self.activityTime(date,activity)
                output.append(sec)

            for productivity in productivityList:
                output.append(self.productivityTime(date,productivity))

            for categoryGroup in categoryGroupList:
                sec = 0
                for category in categoryGroup:
                    sec += self.categoryTime(date,category)
                output.append(sec)

            yield output

class RescueTime:
    def __init__(self,beginDay=None,endDay=None):
        service = Service.Service()
        key = AnalyticApiKey.AnalyticApiKey(open('/home/ysuzuki/MyApplication/rescueapp/rt_key').read(), service)
        parameters = {}
    
        parameters['restrict_kind']  = 'activity'
        #parameters['restrict_kind']  = 'category'
        parameters['perspective']    = 'interval'

        self.today = datetime.datetime.today().strftime("%Y%m%d")
        if beginDay:
            self.beginDay = beginDay
        else:
            self.beginDay = self.today

        if endDay:
            self.endDay = endDay
        else:
            self.endDay = self.today

        parameters["restrict_begin"] = self.beginDay[0:4] + "-" + self.beginDay[4:6] + "-" + self.beginDay[6:8] # %Y%m%d -> %Y-%m-%d
        parameters["restrict_end"] = self.endDay[0:4] + "-" + self.endDay[4:6] + "-" + self.endDay[6:8] # %Y%m%d -> %Y-%m-%d

        self.beginDatetime = datetime.datetime.strptime(self.beginDay,"%Y%m%d")
        self.endDatetime = datetime.datetime.strptime(self.endDay,"%Y%m%d")
        self.dateList = []
        for plusDays in range((self.endDatetime-self.beginDatetime).days+1):
            self.dateList.append((self.beginDatetime+datetime.timedelta(days=plusDays)).strftime("%Y%m%d"))
        
        self.jsonRawData = service.fetch_data(key,parameters)    
        self.data = RescueJSONParser(self.jsonRawData)

    def getTime(self,activityNameList,date=None):
        if not date: date = self.today
        sec = 0
        for activityName in activityNameList:
            try:
                sec += self.data.activityTime(date,activityName)
            except:
                sec += 0
        return sec

    def getProductivityTime(self,date,productivity):
        return self.data.productivityTime(date,productivity)

    def getCategoryTime(self,date,categoryNameList):
        sec = 0
        for categoryName in categoryNameList:
            try:
                sec += self.data.categoryTime(date,categoryName)
            except:
                sec += 0
        return sec

    # ex. activityList = [["Twitter","Tween"],["Hulu","Youtube"]]
    def getAllData(self,activityList,productivityList,categoryList):
        for oneDayData in self.data.fetchAllData(self.dateList,activityList,productivityList,categoryList):
            print oneDayData


if __name__ == "__main__":
    test()
