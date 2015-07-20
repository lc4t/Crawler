# -*- coding:UTF-8 -*-
__author__ = 'lc4t'
import difflib
import sys
import smtplib
from email.mime.text import MIMEText
import Crawler
import time
import filecmp
import re
import threading
class sendMail:
    def __init__(self,content,mailTo,mailHost,mailUser,mailPassword,mailPosfix):
        print ("mailing")
        # self.mailto_list=["lc4t0.0@gmail.com"]
        # self.mail_host="smtp.qq.com"  #设置服务器
        # self.mail_user="lpylzx1@qq.com"    #用户名
        # self.mail_pass=""   #口令
        # self.mail_postfix="qq.com"  #发件箱的后缀
        self.mailto_list = re.split(',| ',mailTo)
        self.mail_host = mailHost  #设置服务器
        self.mail_user = mailUser    #用户名
        self.mail_pass = mailPassword  #口令
        self.mail_postfix = mailPosfix  #发件箱的后缀
        if self.send_mail(self.mailto_list,"new grades",content):
            print "发送成功",
            print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        else:
            print "发送失败",
            print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    def send_mail(self,to_list,sub,content):
        me="Grades"+"<"+self.mail_user+"@"+self.mail_postfix+">"
        msg = MIMEText(content,_subtype='plain',_charset='utf-8')
        msg['Subject'] = sub
        msg['From'] = me
        msg['To'] = ";".join(to_list)
        try:
            server = smtplib.SMTP()
            server.connect(self.mail_host)
            server.login(self.mail_user,self.mail_pass)
            server.sendmail(me, to_list, msg.as_string())
            print to_list
            server.close()
            return True
        except Exception, e:
            print str(e)
            return False


def init(username,password,sleepTime = 600,configList = None):
    fileOld = 'old'+username+'.txt'
    fileNew = 'new'+username+'.txt'
    if (configList):
        mailto_list = str(configList[3].strip('\n'))
        mail_host = str(configList[4].strip('\n'))
        mail_user = str(configList[5].strip('\n'))
        mail_pass = str(configList[6].strip('\n'))
        mail_postfix = str(configList[7].strip('\n'))
    else:
        mailto_list = raw_input("to email address, lc4t0.0@gmail.com:")
        mail_host = raw_input("smtp server,  smtp.qq.com:")
        mail_user = raw_input("mailUser,  lpylzx1@qq.com:")
        mail_pass = raw_input("mailPassword:")
        mail_postfix = raw_input("mailPostfix, qq.com:")
    # while(True):
    try:
        Crawler.init(username,password)
    except Exception as e:
        print (e)
        return
    new = open(fileNew, 'U').readlines()
    try:
        old = open(fileOld, 'r').readlines()
    except:
        old = open(fileOld, 'w+').readlines()
    diff = difflib.ndiff(old,new)

    if (not (filecmp.cmp(fileOld,fileNew))):
        print "not same"
        content = 'studentID= ' + username + ' \n'
        for i in diff:
            content += i
        print content
        sendMail(content,mailto_list,mail_host,mail_user,mail_pass,mail_postfix)
        print "new grades"
        new = open(fileNew,'r')
        old = open(fileOld,'w')
        old.writelines(new.readlines())
    else:
        print "same"
    print "sleeping...@",
    print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    time.sleep(sleepTime)

def getter(existConfigFile):

    existConfigFile = re.split(',| ',existConfigFile)
    args = []
    for configFile in existConfigFile:
        try:
            configList = open(configFile,'rU').readlines()
        except:
            configList = []
        if (configList):
            username = str(configList[0].strip('\n'))
            password = str(configList[1].strip('\n'))
            sleepTime = int(configList[2].strip('\n'))
        else:
            username = raw_input("input your username:")
            password = raw_input("input your password:")
            sleepTime = int(raw_input("input sleep time，600:"))
        args.append([username,password,sleepTime,configList])
    while (True):
        for arg in args:
            init(arg[0],arg[1],arg[2],arg[3])


if __name__ == '__main__':
    existConfigFile = raw_input("your config File:")
    getter(existConfigFile)


