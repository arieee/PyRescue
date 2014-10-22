#!/usr/bin/env python
# -*- coding:utf-8 -*-

from rescuetime.api.service import Service
from rescuetime.api.access import AnalyticApiKey

class activity:
    def __init__(self,data):
        self.date = data[0]
        self.timespent = int(data[1])
        self.num_of_people = int(data[2])
        self.activity = data[3]
        self.category = data[4]
        self.productivity = str(data[5]) #-2,-1,0,1,2
 
class rescuejson:
    def __init__(self,fetch_data):
        self.today_activity_dic = dict()
        self.today_productivity_dic = dict()
        self.today_category_dic = dict()

        for act in fetch_data['rows']:
            a = activity(act)

            if a.activity in self.today_activity_dic:
                self.today_activity_dic[a.activity] += a.timespent
            else:
                self.today_activity_dic[a.activity] = a.timespent

            if a.productivity in self.today_productivity_dic:
                self.today_productivity_dic[a.productivity] += a.timespent
            else:
                self.today_productivity_dic[a.productivity] = a.timespent
            if a.category in self.today_category_dic:
                self.today_category_dic[a.category] += a.timespent
            else:
                self.today_category_dic[a.category] = a.timespent

    def activity_time(self,activity_name):
        return self.today_activity_dic[activity_name]

    def productivity_time(self,productivity_number):
        return self.today_productivity_dic[productivity_number]

    def category_time(self,category_name):
        return self.today_category_dic[category_name]

class rescuetime:
    def __init__(self):
        s = Service.Service()
        k = AnalyticApiKey.AnalyticApiKey(open('/home/ysuzuki/MyApplication/rescueapp/rt_key').read(), s)
        p = {}
    
        p['restrict_kind']  = 'activity'
        p['perspective']    = 'interval'
        d = s.fetch_data(k,p)
        #pp = pprint.PrettyPrinter()
        #pp.pprint(d)
    
        self.todaydata = rescuejson(d)

    def gettime(self,activity_name_list):
        sec = 0
        for activity_name in activity_name_list:
            try:
                sec += self.todaydata.activity_time(activity_name)
            except:
                sec += 0
        return sec

    def productivity_gettime(self,productivity):
        return self.todaydata.productivity_time(productivity)


    def category_gettime(self,category_name_list):
        sec = 0
        for category_name in category_name_list:
            try:
                sec += self.todaydata.category_time(category_name)
            except:
                sec += 0
        return sec

