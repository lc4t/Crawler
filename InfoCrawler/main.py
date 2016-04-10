# -*- coding:UTF-8 -*-
__author__ = 'lc4t'


#------CONFIG-----#
DEBUG = True
availableType = ['weibo', ]
DEFAULT_LOGIN = 'mobile'
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

class WeiboUser:
    '''eg
        id:2656274875   //user id 
        containerid=1005052656274875   // call 
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

    def __init__(self, jsonContent):
        logging.debug('WeiboUser Class init.')
        self.state = False
        try:
            self.rawContent = jsonContent
            self.id = jsonContent['user']['id']
            # self.containerid = re.findall('containerid=(\d+?)&',requests.get('http://m.weibo.cn/u/1618051664?').text)[0]
            self.screen_name = jsonContent['user']['screen_name']
            self.profile_image_url = jsonContent['user']['profile_image_url']
            self.profile_url = jsonContent['user']['profile_url']
            self.verified = jsonContent['user']['verified']
            self.verified_reason = jsonContent['user']['verified_reason']
            self.description = jsonContent['user']['description']
            self.verified_type = jsonContent['user']['verified_type']
            self.gender = jsonContent['user']['gender']
            userinfoText = requests.get('http://m.weibo.cn/page/card?itemid=100505' + str(self.id) + '_-_WEIBO_INDEX_PROFILE_APPS&callback=s').text.encode().decode('unicode-escape')
            self.weibo_count = re.findall('\"count\"\:\"([\d\u4e07]+?)\"\,(\"page_type\"\:\"0\"\,)?\"type\"\:\"weibo\"', userinfoText)[0][0]
            self.follow_count = re.findall('\"count\"\:\"([\d\u4e07]+?)\"\,(\"page_type\"\:\"0\"\,)?\"type\"\:\"attention\"', userinfoText)[0][0]
            self.fans_count = re.findall('\"count\"\:\"([\d\u4e07]+?)\"\,(\"page_type\"\:\"0\"\,)?\"type\"\:\"fans\"', userinfoText)[0][0]
            self.like_count = re.findall('\"count\"\:\"([\d\u4e07]+?)\"\,(\"page_type\"\:\"0\"\,)?\"type\"\:\"like\"', userinfoText)[0][0]
            self.topic_count = re.findall('\"count\"\:\"([\d\u4e07]+?)\"\,(\"page_type\"\:\"0\"\,)?\"type\"\:\"topic\"', userinfoText)[0][0]
            self.state = True
        except Exception as EWeiboUser:
            logging.debug('Error in WeiboUser: ' + str(EWeiboUser))
            
    def printUserinfo(self):
        if (self.state == True):
            print ('-->Userinfo Start<--')
            print ('id----------------->' + str(self.id))
            print ('screen_name-------->' + str(self.screen_name))
            print ('profile_image_url-->' + str(self.profile_image_url))
            print ('profile_url-------->' + str(self.profile_url))
            print ('verified----------->' + str(self.verified))
            print ('verified_reason---->' + str(self.verified_reason))
            print ('description-------->' + str(self.description))
            print ('verified_type------>' + str(self.verified_type))
            print ('gender------------->' + str(self.gender))
            print ('weibo_count-------->' + str(self.weibo_count))
            print ('follow_count------->' + str(self.follow_count))
            print ('fans_count--------->' + str(self.fans_count))
            print ('like_count--------->' + str(self.like_count))
            print ('topic_count-------->' + str(self.topic_count))
            print ('fans_count--------->' + str(self.fans_count))
            print ('--> Userinfo End <--')
        else:
            if (DEBUG):
                print ('Userinfo State: ' + str(self.state))


class WeiboMessage:
    '''eg.
        id:123123123
        type: weibo
        created_timestamp: 0
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
        logging.debug('Message Class init.')
        self.state = False
        self.rawContent = content
        content = content
        self.Type = str(Type)
        if ('weibo' in Type):
            try:
                self.id = content['mblog']['id']
                self.created_timestamp = content['mblog']['created_timestamp']
                self.author = content['mblog']['user']['id']  # foreign key
                self.text = content['mblog']['text']
                self.pic_ids = content['mblog']['pic_ids']
                self.source = content['mblog']['source']
                self.selfLink = content['scheme']
                self.reposts_count = content['mblog']['reposts_count']
                self.comments_count = content['mblog']['comments_count']
                self.attitudes_count = content['mblog']['attitudes_count']
                self.state = True
                self.topicURL = None
                self.topic = None
                self.shortLink = []
                self.fullLink = []
                self.linkType = []
                try:
                    topicFind = re.findall('<a class="k" href="([/%\w\W\d\?=]+)">#(.+)#<\/a>', s)
                    if (topicFind):
                        self.topicURL = topicFind[0][0]
                        self.topic = topicFind[0][1]


                    linkFind = re.findall('<a data-url="(http://t.cn/[\w\W\d]+?)" href="(.*?)" ><i.*?</i><span class="surl-text">(.*?)</span></a>', s)
                    if (linkFind):
                        for one in linkFind:
                            self.shortLink.append(one[0])
                            self.fullLink.append(one[1].replace('http://weibo.cn/sinaurl?u=','http://'))
                            self.linkType.append(one[2])
                except Exception as eWeiboMessageNoTopicOrLink:
                    logging.debug('Error in find topic or link in weibo message' + str(eWeiboMessageNoTopicOrLink))
            except Exception as eWeiboMessage:
                logging.error('Error in Init weibo message:' + str(eWeiboMessage))
                logging.debug(content)
        else:
            logging.error('Error in Init message, cannot find.')
    
    def getState(self):
        return self.state
    
    def getType(self):
        return self.Type
    
    def printWeiboMessage(self):
        if (self.state == True):
            print ('Message Type: ' + self.Type)
            print ('-->Message Start<--')
            print ('id---------------->' + str(self.id))
            print ('created_timestamp->' + str(self.created_timestamp))
            print ('author------------>' + str(self.author))
            print ('text-------------->' + self.text)
            print ('source------------>' + self.source)
            if (len(self.pic_ids) > 0):
                print ('pic_ids----------->' + '\npic_ids----------->'.join(self.pic_ids))
            if self.topicURL:
                print ('topicURL---------->' + str(self.topicURL))
                print ('topic------------->' + str(self.topic))
            for i in range(0, len(self.shortLink), 1):
                print ('>>shortLink------->' + self.shortLink[i])
                print ('>>fullLink-------->' + self.fullLink[i])
                print ('>>linkType-------->' + self.linkType[i])

            print ('selfLink---------->' + self.selfLink)
            print ('reposts_count----->' + str(self.reposts_count))
            print ('comments_count---->' + str(self.comments_count))
            print ('attitudes_count--->' + str(self.attitudes_count))
            print ('-->Message End  <--' + str(self.attitudes_count))
        else:
            if (DEBUG):
                print ('Message Type: ' + self.Type)
                print ('Message State: ' + str(self.state))





class Weibo:
    '''
        follow weibo.cn 's define
    '''
    def __init__(self, jsonContent):
        try:
            logging.debug('Weibo Class init.')
            # self.filter = []
            self.hotmblog = []
            # self.follow_mblog = []
            self.mblog = []
            self.more_hot_mblog = []
            self.usersList = []
            for card in jsonContent['cards']:
                # print (card)
                if (card['itemid'] == 'filter'):
                    pass
                elif (card['itemid'] == 'follow_mblog'):
                    pass
                elif (card['itemid'] == 'relatedUserSelect'):
                    pass
                elif (card['itemid'] == 'hotmblog'):
                    for messageI in card['card_group']:
                        if ('mblog' not in messageI): continue
                        message = WeiboMessage('weibo_hotmblog', messageI)
                        self.hotmblog.append(message)
                elif (card['itemid'] == 'mblog'):
                    for messageI in card['card_group']:
                        # if ('mblog' not in message): continue
                        message = WeiboMessage('weibo_mblog', messageI)
                        self.mblog.append(message)
                elif (card['itemid'] == 'more_hot_mblog'):
                    for messageI in card['card_group']:
                        if ('mblog' not in messageI): continue
                        message = WeiboMessage('weibo_more_hot_mblog', messageI)
                        self.more_hot_mblog.append(message)
                elif (card['itemid'] == 'user'):
                    for userI in card['card_group']:    
                        user = WeiboUser(userI)
                        self.usersList.append(user)
                else:
                    logging.error('New itemid in cards, please edit it: ' + card['itemid'])
        except Exception as eWeibo:
            logging.error('Cannot init Weibo Class: ' + str(eWeibo))
    
    def handle(self, method = 'print'):
        if (method == 'print'):
            for i in self.hotmblog:
                i.printWeiboMessage()
            # for i in self.follow_mblog:
            #     i.printMessage()
            for i in self.mblog:
                i.printWeiboMessage()
            for i in self.more_hot_mblog:
                i.printWeiboMessage()
            for i in self.usersList:
                i.printWeiboMessage()

class WebsiteFactory:
    def __init__(self):
        logging.debug('Class WebsiteFactory init')
    
    def selector(self, selectType):
        try:
            if ('weibo' in selectType):
                logging.info('select weibo.com')
                return WebsiteWeiboCom()
            elif ('baidu' in selectType):
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
        self.method = 'mobile'
    
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
        except Exception as ex:
            logging.error('Wrong in return a search.')
            logging.debug(ex)
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
                self.request.get(redirectURL).text
                return True
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
            # return self.driver.page_source
            return True
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
            self.request.get(loginURL).text  #
            return True
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
        try:
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
            result = queryANS.text.replace('false', 'False').replace('true', 'True').replace('null', 'None').replace('\/', '/')
            result = eval(result)
            return Weibo(result)
        except Exception as eSearch:
            logging.error('Error in search function: ' + str(eSearch))
            return None
'''




'''

class Controller:
    def __init__(self):
        print ('Welcome to this crawler--->')

    def control(self):
        
        inputControlCharText = '''
                                Main control
                                --->1: select type
                                --->2: login
                                --->3: search
                                --->c: return back
                                '''
        inputControlChar = input(inputControlCharText)
        while (inputControlChar != 'exit'):
            if (inputControlChar == '1'):
                self.selector()
            elif (inputControlChar == '2'):
                self.loginer(self.Type)
            elif (inputControlChar == '3'):
                self.search()
            elif (inputControlChar == 'c'):
                return

            else:
                print ('Wrong input')
            inputControlChar = input(inputControlCharText)
    def selector(self):
        inputType= ''
        while (inputType not in availableType):
            inputType = input('Input type from  ' + str(availableType) + ': ')
        self.Type = inputType
        if (inputType == availableType[0]):
            #weibo
            self.process = WebsiteFactory().selector('weibo.com')
        else:
            pass

    def loginer(self, value):
        inputUsername = input('Input username: ')
        inputPassword = input('Input password: ')
        while (not self.process.login(inputUsername, inputPassword, DEFAULT_LOGIN)):
            inputNumText = '''
                            Cannot login, please check log.
                            --->1: reInput username
                            --->2: reInput password
                            -->12: reInput both
                            '''
            
            inputNum = input(inputNumText)
            if ('1' in inputNum):
                inputUsername = input('Input username: ')
            if ('2' in inputNum):
                inputPassword = input('Input password: ')
        print ('login success')
    def search(self):
        inputQueryTypeText = '''input search type:'''
        inputQueryValueText = '''input search query:'''

        search = self.process.search(input(inputQueryTypeText), input(inputQueryValueText))
        search.handle('print')


def main():
    # eg = Controller()
    # eg.control()

    eg = WebsiteFactory().selector('weibo.com')
    eg.login('weibo@lc4t.me', 'lc4t@2016')
    ans = eg.search('all', '新闻')
    ans.handle()

if __name__ == '__main__':
    main()

'''
http://m.weibo.cn/unread?t=1459258275363
unix timestamp with 3 points,delete point

'''