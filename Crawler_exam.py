# -*- coding:utf-8 -*-
__author__ = 'lc4t'

import Crawler

uestc = Crawler.UESTC("2014060102018","")
uestc.getIndex()
uestc.getEAS()
print uestc.getCources(True)



