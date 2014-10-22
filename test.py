#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import pprint
sys.path.append('./')

import pprint
#import pandas as pd
from rescuetime.api.service import Service
from rescuetime.api.access import AnalyticApiKey
 
s = Service.Service()
k = AnalyticApiKey.AnalyticApiKey(open('rt_key').read(), s)
p = {}
pp = pprint.PrettyPrinter()
 
p['restrict_begin'] = '2014-05-11'
p['restrict_end'] = '2014-05-11'
p['restrict_kind']  = 'activity'
p['perspective']    = 'interval'
d = s.fetch_data(k,p)

pp.pprint(d)

