# -*- coding:UTF-8 -*-
__author__ = 'lc4t'


#------CONFIG-----#

#------END--------#

#------import-----#
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s] [thread: %(threadName)s] [ID: %(thread)d] [module: %(module)s] [function:%(funcName)s] [line: %(lineno)d] [%(levelname)s: %(message)s]',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='InfoCrawler.log',
                    filemode='w')


import base64
import binascii
import re
import requests
import rsa
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from urllib.parse import unquote
from urllib.parse import urlencode

#------END--------#

class User:
    '''eg
        id:2656274875   //user id 
        containerid=1005052656274875   // call 
        source: weibo
        screen_name: pig
        profile_image_url:http://tp4.sinaimg.cn/1/1/1
        profile_url:/u/2656274875
        verified:True
        verified_reason:pig
        description:new pig
        verified_type:1
        gender:
        weibo_count:statuses_count:1223
        follow_count:
        fans_count:
        like_count:
        topic_count:


    基本信息：http://m.weibo.cn/page/card?itemid=1005052656274875_-_WEIBO_INDEX_PROFILE_APPS&callback=_1459705215087_4
    微博:http://m.weibo.cn/page/card?itemid=1005052656274875_-_WEIBO_INDEX_PROFILE_WEIBO_GROUP_OBJ&callback=_1459705466830_7
    相册:http://m.weibo.cn/page/card?itemid=1005052656274875_-_WEIBO_INDEX_PROFILE_PHOTOS&callback=_1459705466830_8
    
    '''

    def __init__(self):
        pass

class Message:
    '''eg.
        id:123123123
        type: weibo
        created_timestamp: yyyy-yy-dd
        author: foreign-key--userid
        text: whoami
        source:weibo.com
        reposts_count:
        link: 
        keyword: pig
        reposts_count:转发
        comments_count:评论
        attitudes_count:赞
    '''
    def __init__(self, Type, content):

        self.rawContent = content
        self.Type = Type
        
        if (Type == 'weibo'):
            pass
    def getType(self):
        return self.Type





class Weibo:
    '''
        follow weibo.cn 's define
    '''
    def __init__(self, jsonContent):
        self.filter = []
        self.hotmblog = []
        self.follow_mblog = []
        self.mblog = []
        for card in jsonContent['cards']:
            # print (card)
            if (card['itemid'] == 'filter'):
                for message in card['group']:
                    self.filter.append(message)
            elif (card['itemid'] == 'hotmblog'):
                for message in card['card_group']:
                    self.hotmblog.append(message)
            elif (card['itemid'] == 'follow_mblog'):
                for message in card['card_group']:
                    self.follow_mblog.append(message)
            elif (card['itemid'] == 'mblog'):
                for message in card['card_group']:
                    self.mblog.append(message)
            else:
                logging.error('New itemid in cards, please edit it: ' + card['itemid'])
    def process(self):

    


class WebsiteFactory:
    def __init__(self):
        logging.debug('Class WebsiteFactory init')
    def selector(self, selectType):
        try:
            if (selectType == 'weibo.com'):
                logging.info('select weibo.com')
                return WebsiteWeiboCom()
            elif (selectType == 'baidu'):
                logging.info('select baidu')
                return WebsiteBaidu()
            else:
                raise AttributeError('No match found.')
        except Exception as e:
            logging.error('Do not match a website to crawler.')
            logging.debug(e)
            return None





class WebsiteWeiboCom(WebsiteFactory):
    def __init__(self):
        logging.debug('Class WebsiteWeiboCom init')
        self.request = requests.Session()
        self.method = 'requests'
    
    def getRSAPassword(self, pubkey, servertime, nonce, password, key = 65537):
        rsaPublickey = int(pubkey, 16)
        key = rsa.PublicKey(rsaPublickey, key)
        message = str(servertime) + '\t' + str(nonce) + '\n' + str(password)
        password = rsa.encrypt(message.encode(), key)
        password = binascii.b2a_hex(password)
        return password.decode()

    def login(self, username, password, method = 'init'):
        if (method == 'init'):
            method = self.method
        else:
            self.method = method
        try:
            if (method == 'requests'):
                return self.loginByRequests(username, password)
            elif (method == 'webdriver'):
                return self.loginByWebdriver(username, password)
            elif (method == 'mobile'):
                return self.loginByMobile(username, password)
            else:
                raise AttributeError('No match found')

        except Exception as e:
            logging.error('Do not match a method to crawler')
            logging.debug(e)
            return None

    def search(self, type, query, method = 'init'):
        '''need params to search
            type
            query
        '''
        if (method == 'init'):
            method = self.method
        else:
            self.method = method
        try:
            if (method == 'requests'):
                return self.searchByRequests(type, query)
            elif (method == 'webdriver'):
                return self.searchByWebdriver(type, query)
            elif (method == 'mobile'):
                return self.searchByMobile(type, query)
            else:
                raise AttributeError('No match found')
        except Exception as e:
            logging.error('Wrong in return a search.')
            logging.debug(e)
            return None

    def loginByRequests(self, username, password):
        logging.info('login Start by Requests')
        '''-->1
            need params:
                        su: base64.b64encode((urlencode({'su':USERNAME}).split('=')[1]).encode()).decode()
                            # username -> urlencode -> base64
                        _ : int(time.time())
                            # this is Unix timestamp, integer
        '''
        try:
            su = base64.b64encode((urlencode({'su':username}).split('=')[1]).encode()).decode()
        except Exception as e:
            logging.error('username invalid')
            logging.debug(e)
            logging.debug(username)
            return None

        _ = int(time.time())
        usernameRequestURL = 'http://login.sina.com.cn/sso/prelogin.php'
        params = {
            'entry'     : 'weibo',
            'callback'  : 'sinaSSOController.preloginCallBack',
            'su'        : su,
            'rsakt'     : 'mod',
            'checkpin'  : '1',
            'client'    : 'ssologin.js(v1.4.18)',
            '_'         : _,
        }

        try:
            logging.info('prelogin request start:' + usernameRequestURL)
            usernameRequest = self.request.get(usernameRequestURL, params = params)
            response = usernameRequest.text
        except Exception as e:
            logging.error('Cannot get RSA key')
            logging.debug(e)
            return None
        '''-->2
            need params from web to encrypt password, get them from usernameRequest:
                        servertime
                        nonce
                        pubkey
                        rsakv
        '''
        try:
            preloginDict = eval(re.findall('\{.*\}',response)[0])
            # print (preloginDict)
            servertime  = preloginDict['servertime']
            nonce       = preloginDict['nonce']
            pubkey      = preloginDict['pubkey']
            rsakv       = preloginDict['rsakv']
            params = {
                'entry':'weibo',
                'gateway':'1',
                'from':'',
                'savestate':'7',
                'useticket':'1',
                'pagerefer':'http://passport.weibo.com/visitor/visitor?entry=miniblog&a=enter&url=http%3A%2F%2Fweibo.com%2F&domain=.weibo.com&ua=php-sso_sdk_client-0.6.14&_rand=1458317776.8514',
                'vsnf':'1',
                'su':su,
                'service':'miniblog',
                'servertime':servertime,
                'nonce':nonce,
                'pwencode':'rsa2',
                'rsakv':rsakv,
                'sp':self.getRSAPassword(pubkey, servertime, nonce, password),
                'sr':'1600*900',
                'encoding':'UTF-8',
                'prelt':'1311',
                'url':'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
                'returntype':'META'
            }
        except Exception as e:
            logging.error('Cannot analyze preloginDict')
            logging.debug(e)
            return None


        '''-->3
            login
        '''
        try:
            loginURL = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)'
            loginRequest = self.request.post(loginURL, params = params)
            locationURL = re.findall("location.replace\([\'\"](http://.*?)[\'\"]\)", loginRequest.text)[0]
            '''-->3.1
                login success, visit the page
            '''
            if (re.findall('retcode=0', locationURL)[0]):
                redirectURL =  re.findall('"redirect":"(.*)"', self.request.get(locationURL).text)[0].replace('\\', '')
                print (self.request.get(redirectURL).text)

        except Exception as e:
            logging.error('Cannot Login')
            logging.debug(e)
            '''-->3.2
                if login fail, find reason
            '''
            try:
                reason = re.findall('reason=((%[a-zA-Z0-9]{2})+)', locationURL)[0][0]
                reason = unquote(reason, encoding='gbk')
                logging.error('cannot login:' + reason)
            except Exception as e:
                logging.error('Find cannot login reason error, may be login success')
                logging.debug(e)
            return None

    def loginByWebdriver(self, username, password):
        try:
            logging.info('login Start by webdriver')
            # PhantomJS
            self.driver = webdriver.PhantomJS()
            self.driver.set_window_size(1600, 900)
            logging.info('visit http://weibo.com by webdriver')
            self.driver.get("http://weibo.com")
            time.sleep(20)  # wait for weibo.com load
            logging.info('try to input by webdriver')
            usernameInput = self.driver.find_element_by_name("username")
            passwordInput = self.driver.find_element_by_name("password")
            self.driver.find_element_by_xpath('//a[@action-data=\'type=normal\']').click()
            usernameInput.click()
            usernameInput.send_keys(username)
            usernameInput.send_keys(Keys.TAB)
            time.sleep(1)   # wait for prelogin
            passwordInput.send_keys(password)
            self.driver.find_element_by_xpath('//a[@action-type=\'btn_submit\']').click()
            logging.info('input done by webdriver')
            logging.info('try login by webdriver')
            time.sleep(20)  # wait for loading content
            logging.info('login success')
            # print (self.driver.page_source)
            return self.driver.page_source
        except Exception as e:
            logging.error('Cannot login')
            logging.debug(e)

    def loginByMobile(self, username, password):

        preloginURL = 'https://passport.weibo.cn/sso/login'
        loginURL = 'http://m.weibo.cn/'
        headers = {
            'Accept':'*/*',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'en-US,en;q=0.8',
            'Connection':'keep-alive',
            'Content-Type':'application/x-www-form-urlencoded',
            'Origin':'https://passport.weibo.cn',
            'Referer':'https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=http%3A%2F%2Fm.weibo.cn%2F',
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36'
        }
        params = {
            'username': username,
            'password': password,
            'savestate':'1',
            'ec':'0',
            'pagerefer':'https://passport.weibo.cn/signin/welcome?entry=mweibo&r=http%3A%2F%2Fm.weibo.cn%2F&wm=3349&vt=4',
            'entry':'mweibo',
            'wentry':'',
            'loginfrom':'',
            'client_id':'',
            'code':'',
            'qq':'',
            'hff':'',
            'hfp':'',
        }
        try:
            preloginRequest = self.request.post(preloginURL, data = params, headers = headers)
            setcookiesURL = eval(preloginRequest.text)['data']['crossdomainlist']
            weiboComSet = self.request.get('https:' + setcookiesURL['weibo.com'].replace('\\', ''))
            weiboCnSet = self.request.get('https:' + setcookiesURL['weibo.cn'].replace('\\', ''))
            sinaSet = self.request.get('https:' + setcookiesURL['sina.com.cn'].replace('\\', ''))



            return self.request.get(loginURL).text
        except Exception as e:
            '''
                try to find why can not login
            '''
            try:
                reason = eval(preloginRequest.text)['msg']
                logging.error('Cannot login:' + reason)
            except Exception as e:
                logging.error('Cannot login & Cannot find why cannot login')
                logging.debug(e)
            logging.debug(e)
            return None

    def searchByMobile(self, Type, query):
        '''need params to search 
            # get
            type: all/user/wb
            query: user
        '''
        if (Type == 'all'):
            typeCode = '1'
        elif (Type == 'user'):
            typeCode = '3'
        elif (Type == 'wb' or Type == 'weibo'):
            Type = 'wb'
            typeCode = '2'
        else:
            Type = 'all'
            typeCode = '1'
            logging.error('method error:' + str(Type) + ' is invalid, use \'all\'')
        # queryURL = 'http://m.weibo.cn/searchs/result'
        # params = {
        #     'type':Type,
        #     'queryVal':str(query)
        # }
        # queryANS = self.request.get(queryURL, params = params)
        # print (queryANS.text)

        queryURL = 'http://m.weibo.cn/page/pageJson'
        params = {
            'containerid':'100103type=' + typeCode + '&q=' + str(query),
            'type':str(Type),
            'queryVal':str(query),
            'title':str(query),
            'v_p':11,
            'ext':'',
            'fid':'100103type=' + typeCode + '&q=' + str(query),
            'uicode':10000011,
            'next_cursor':'',
            'page':1,
        }
        queryANS = self.request.get(queryURL, params = params)
        result = queryANS.text.replace('false', 'False').replace('true', 'True').replace('null', 'None')
        result = eval(result)
        return Weibo(result)
        
'''




'''





def main():
    weibo = WebsiteFactory().selector('weibo.com')
    weibo.login('weibo@lc4t.me', 'lc4t@2016', 'mobile')
    weibo.search('all', '新闻')

if __name__ == '__main__':
    main()

'''
http://m.weibo.cn/unread?t=1459258275363
unix timestamp with 3 points,delete point

'''