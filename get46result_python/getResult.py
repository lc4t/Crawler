# -*- coding:utf-8 -*-
__author__ = 'lc4t'
# import urllib
import urllib.request
import urllib.parse
import http.cookiejar
import xlwt
import xlutils
# import urllib.error
import re
from bs4 import BeautifulSoup

def make_cookie(name, value):
    return http.cookiejar.Cookie(
        version=0,
        name=name,
        value=value,
        port=None,
        port_specified=False,
        domain="xxxxx",
        domain_specified=True,
        domain_initial_dot=False,
        path="/",
        path_specified=True,
        secure=False,
        expires=None,
        discard=False,
        comment=None,
        comment_url=None,
        rest=None
    )

class Query:
    def __init__(self):
        pass
    def Sushe(self, ticket, name):
        ticket = str(ticket)
        name = urllib.parse.quote(name)
        url = 'http://www.chsi.com.cn/cet/query?zkzh='+ticket+'&xm='+name
        headers = {
        'Host': 'www.chsi.com.cn',
        # 'Proxy-Connection': 'keep-alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
        'Referer': 'http://www.chsi.com.cn/cet/',
        # 'Accept-Encoding': 'gzip, deflate, sdch',
        # 'Accept-Language': 'en-US,en;q=0.8',
        # 'Content-Length': '2'
        }
        request = urllib.request.Request(url,headers=headers)
        result = urllib.request.urlopen(request)
        # cookies = http.cookiejar.CookieJar()
        # postdata = urllib.parse.urlencode({'id':'510020151202724','name':'陈钰林'}).encode('utf-8')
        # headers = {
        #     'Host': 'cet.99sushe.com',
        #     'Proxy-Connection': 'keep-alive',
        #     'Content-Length': '36',
        #     'Cache-Control': 'max-age=0',
        #     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        #     'Origin': 'http://cet.99sushe.com',
        #     'Upgrade-Insecure-Requests': '1',
        #     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
        #     'Content-Type': 'application/x-www-form-urlencoded',
        #     'Referer': 'http://cet.99sushe.com/',
        #     'Accept-Encoding': 'gzip, deflate',
        #     'Accept-Language': 'en-US,en;q=0.8'

        # }
        # request = urllib.request.Request(url, postdata,headers)
        # cookie = http.cookiejar.CookieJar()
        # cookie.set_cookie(make_cookie('score',''))
        # opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie))
        # result = opener.open(request)

        # print (result.read().decode('utf-8'))
        html = BeautifulSoup(result.read())
        p = html.find_all(class_='cetTable')
        ans = p[0].get_text()
        return ans.replace(' ','').replace('\n','').replace('\t','').replace('\r','').replace('姓名：',' ').replace('学校：',' ').replace('考试类别：',' ').replace('准考证号：',' ').replace('考试时间：',' ').replace('总分：',' ').replace('听力：',' ').replace('阅读：',' ').replace('写作与翻译：',' ')


class CreateXLS:
    def __init__(self, fileName, sheetName):
        self.fileName = fileName
        self.workBook = xlwt.Workbook(encoding = 'utf-8')
        self.workSheet = self.workBook.add_sheet(sheetName, cell_overwrite_ok = False)
    def Save(self):
        self.workBook.save(self.fileName)
    def Write(self,row,column,value):
        self.workSheet.write(row,column,value)
        self.Save()

# class WriteXLS():
#     def __init__(self):
#         xls = xlwt.open_workbook('46.xls')
#         sheet = xls.sheet_by_index(0)
#         sheet.write(2,1,'test')

test = Query()
ans = test.Sushe()
print (ans.split())

q = CreateXLS('46.xls','Sheet1')
# q.Write(2,3,'test')


## what next:   read the xls, copy and add grade list