# -*- coding:UTF-8 -*-
__author__ = 'lc4t'
import difflib
import sys
import smtplib
from email.mime.text import MIMEText
import Crawler
import time
import filecmp
class sendMail:
    def __init__(self,content,mailTo,mailHost,mailUser,mailPassword,mailPosfix):
        print ("mailing")
        # self.mailto_list=["lc4t0.0@gmail.com"]
        # self.mail_host="smtp.qq.com"  #设置服务器
        # self.mail_user="lpylzx1@qq.com"    #用户名
        # self.mail_pass=""   #口令
        # self.mail_postfix="qq.com"  #发件箱的后缀
        self.mailto_list = [mailTo]
        self.mail_host = mailHost  #设置服务器
        self.mail_user = mailUser    #用户名
        self.mail_pass = mailPassword  #口令
        self.mail_postfix = mailPosfix  #发件箱的后缀
        if self.send_mail(self.mailto_list,"new grades",content):
            print "发送成功"
        else:
            print "发送失败"
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
            server.close()
            return True
        except Exception, e:
            print str(e)
            return False


def init(username,password,sleepTime = 600):
    fileOld = 'old'+username+'.txt'
    fileNew = 'new'+username+'.txt'
    mailto_list=raw_input("to email address, lc4t0.0@gmail.com:")
    mail_host=raw_input("smtp server,  smtp.qq.com:")
    mail_user=raw_input("mailUser,  lpylzx1@qq.com:")
    mail_pass=raw_input("mailPassword:")
    mail_postfix=raw_input("mailPostfix, qq.com:")
    while(True):
        try:
            Crawler.init(username,password)
        except Exception as e:
            print (e)
            continue
        new = open(fileNew, 'U').readlines()
        try:
            old = open(fileOld, 'r').readlines()
        except:
            old = open(fileOld, 'w+').readlines()
        diff = difflib.ndiff(old,new)

        if (not (filecmp.cmp(fileOld,fileNew))):
            print "not same"
            content = ""
            for i in diff:
                content += i
            print content
            mail = sendMail(content,mailto_list,mail_host,mail_user,mail_pass,mail_postfix)
            print "new grades"
            new = open(fileNew,'r')
            old = open(fileOld,'w')
            old.writelines(new.readlines())
        else:
            print "same"
        print "sleeping..."
        time.sleep(sleepTime)

if __name__ == '__main__':
    username = raw_input("input your username:")
    password = raw_input("input your password:")
    sleepTime = int(raw_input("input sleep time，600:"))
    init(username,password,sleepTime)
