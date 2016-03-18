# -*- coding:UTF-8 -*-
__author__ = 'lc4t'


#------CONFIG-----#

#------END--------#

#------import-----#
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s] [thread: %(threadName)s] [ID: %(thread)d] [module: %(module)s] [function:%(funcName)s] [line: %(lineno)d] [%(levelname)s: %(message)s]',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='WeiboCrawler.log',
                    filemode='w')

# logging.debug('debug message')
# logging.info('info message')
# logging.warning('warning message')
# logging.error('error message')
# logging.critical('critical message')
# import lxml
import base64
import binascii
import re
import requests
import rsa
import time
from urllib.parse import unquote
from urllib.parse import urlencode
# from bs4 import BeautifulSoup
#------END--------#




class WebsiteFactory:
    def __init__(self):
        logging.debug('Class WebsiteFactory init')
    def selector(self, selectType):
        try:
            if (selectType == 'weibo.com'):
                logging.info('select weibo.com')
                return WebsiteWeiboCom()
            else:
                raise AttributeError('No match found.')
        except Exception as e:
            logging.error('Do not match a website to crawler.')
            logging.debug(e)





class WebsiteWeiboCom(WebsiteFactory):
    def __init__(self):
        logging.debug('Class WebsiteWeiboCom init')
        self.request = requests.Session()
    def getRSAPassword(self, pubkey, servertime, nonce, password, key = 65537):
        rsaPublickey = int(pubkey, 16)
        key = rsa.PublicKey(rsaPublickey, key)
        message = str(servertime) + '\t' + str(nonce) + '\n' + str(password)
        password = rsa.encrypt(message.encode(), key)
        password = binascii.b2a_hex(password)
        return password.decode()
    def login(self, username, password):
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
                return self.request.get(redirectURL)
        except Exception as e:
            logging.error('Cannot Login')
            logging.debug(e)
            '''-->3.2
                if login fail, find reason
            '''
            try:
                reason = re.findall('reason=((%[a-zA-Z0-9]{2})+)', locationURL)[0][0]
                reason = unquote(reason, encoding='gbk')
                logging.info('cannot login:' + 'reason')
                return None
            except Exception as e:
                logging.info('Find cannot login reason error, may be login success')
                logging.debug(e)
            return None


def main():
    weibo = WebsiteFactory().selector('weibo.com')
    weibo.login('weibo@lc4t.me', 'lc4t')

if __name__ == '__main__':
    main()
