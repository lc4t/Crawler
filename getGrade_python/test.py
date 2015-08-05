# -*- coding:utf-8 -*-
__author__ = 'lc4t'

import urllib
import urllib2
import cookielib
import json

loginURL = "http://219.243.39.24/wctju3/Admin.aspx"
cookies = cookielib.CookieJar()
ID = 3013205004
postData = urllib.urlencode(
            {
            '__EVENTTARGET':'',
            '__EVENTARGUMENT':'',
            '__LASTFOCUS':'',
            '__VIEWSTATE':'/wEPDwUJMjI1OTI3OTQ2D2QWAgIBD2QWDAIFDw8WAh4EVGV4dAUGMTM0MjQ5ZGQCDw8PZBYEHgtvbm1vdXNlb3ZlcgUcdGhpcy5zdHlsZS5jb2xvcj0ncm95YWxibHVlJx4Kb25tb3VzZW91dAUXdGhpcy5zdHlsZS5jb2xvcj0nbmF2eSdkAhEPDxYCHwAFATBkZAIWDw9kFgQfAQUcdGhpcy5zdHlsZS5jb2xvcj0ncm95YWxibHVlJx8CBRd0aGlzLnN0eWxlLmNvbG9yPSduYXZ5J2QCFw8PZBYEHwEFHHRoaXMuc3R5bGUuY29sb3I9J3JveWFsYmx1ZScfAgUXdGhpcy5zdHlsZS5jb2xvcj0nbmF2eSdkAicPDxYCHwAFCemZiOe7p+S8n2RkZOZNJsooK7JCIi+aVnmd7TBg5f9/xB84PtnmEcRsBs07',
            '__EVENTVALIDATION':'/wEWQgKzrPuZCgLgpLfQDwKtva7mBQKvleWTDQKRld6RBQKs/vumDwKDkYzaAgKhnKD/AQL18PCwBQLWuZjWBQKy3rPNAgKp463JCgK/we+VCwKbr/fJBAL13+GcBALw08XEDALLoPOQCgL3/YzaCwLYvZePCwLplNi7BQKg++r3AwKir9C/DAKwmZz4DwLAt9ehCALa/q6nCwKct4jLAQKM54rGBgLJmu8OAsj3m5kDAte51rQCAoKpu7UOAqvvlNkLAovT8sMEAv+80ZsHAoXg6qwPAuPQ5/0HApeZ2aUJAr6V5LsHApm73bwHAva61rQCAoOpu7UOAoyN88MEAr710ZsHAoSa66wPAquavfUJArXLmiYCr8aT7wcC7pLFqw0ChfuyogQChc66/AECpPvO2ggC0uOV1AkCpIno/QcCyPefmQMC7NGy6wYC7NH22QwCsPvq9wMC0JK1xwUCgZPFqw0ChfvK4gcC0NeeggYCuOPBhAoClJns9AkC0P/m4gICqeOlxQcCwcfPqwNGaxjoCmEEGCCJIvlcPD/nA983DMIeq7Z/poVM1Arz0w==',
            'txtXMBH':'',
            'txtNewSFZHxs':'',
            'txtNewNameXS':'',
            'btnXSname':'',
            'txtXH':ID,
            'txtNewSFZH':'',
            'txtNewName':'',
            'txt13_tax_already':'',
            'txt13Tax_bu':'',
            'txt13Tax':'',
            'txt13_income':'',
            'txt13_out_tax':'',
            'txt13_tju_tax':'',
            'txt13_out_income':'',
            'txt13_tju_income':'',
            'txt12Tax_bu':'',
            'txt12Tax':'',
            'txt12_out_tax':'',
            'txt12_tju_tax':'',
            'txt12_out_income':'',
            'txtContent':'',
            'txtNo':'',
            'txtCL':'',
            'txt12_tju_income':'',
            'TextBox1':'',
            'TextBox2':'4',
            'txtXX':'',
            'txtfor':'',
            'txtGZBH':'',
            'txtBMBH':''
            })
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies))
request = urllib2.Request(url = loginURL,data = postData)
result = opener.open(request)
print result.read()



