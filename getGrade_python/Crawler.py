# -*- coding:UTF-8 -*-
__author__ = 'lc4t'
import urllib
import urllib2
import re
import sys
import cookielib
from bs4 import BeautifulSoup

def judgeExistMakeupGrade(gradeList):   #into is tempA, no u'',
    for i in xrange(0,len(gradeList),8):    # to 8
        if (re.findall(u'--',gradeList[6])):
            return 1
    return 0

class TermStruct:

    def __init__(self):
        self.__length__ = 0
        self.academicYear = []
        self.term = []
        self.numberOfCources = []
        self.totalCredit = []
        self.gpa = []
        self.all = []
        self.time = []
    def add(self, Academic_Year, Term, Number_Of_Cources, Total_Credit, GPA):
        self.academicYear.append(Academic_Year)
        self.term.append(Term)
        self.numberOfCources.append(Number_Of_Cources)
        self.totalCredit.append(Total_Credit)
        self.gpa.append(GPA)
        self.__length__ += 1

    def addList(self,list):
        self.academicYear.append(list[0])
        self.term.append(list[1])
        self.numberOfCources.append(list[2])
        self.totalCredit.append(list[3])
        self.gpa.append(list[4])
        self.__length__ += 1

    def addFinal(self,allGPA,time):
        self.all = allGPA
        self.time = time

    def getFinal(self):
        return [self.all,self.time]

    def printAll(self):
        for i in xrange(0,self.__length__,1):
            print self.academicYear[i],
            print "第",
            print self.term[i],
            print "学期 共",
            print self.numberOfCources[i],
            print "门课 总学分",
            print self.totalCredit[i],
            print "平均绩点",
            print self.gpa[i]

    def printFinal(self):
        print "总课程数:",self.all[0],
        print "总学分:",self.all[1],
        print "总评绩点:",self.all[2]
        # print "统计时间:",self.time[0]

    def getTerm(self, number):
        return ([self.academicYear[number], self.term[number], self.numberOfCources[number],
                 self.totalCredit[number], self.gpa[number]])

    def getCourseNumber(self):
        return self.all[0]

class Courcestruct:

    def __init__(self):
        self.count = 0
        self.academicYear = []
        self.semester = []
        self.courceCode = []
        self.courceNumber = []
        self.courceName = []
        self.courceType = []
        self.courceCredit = []
        self.courceGrade = []
        self.courceFinal = []
        self.courceGPA = []
        self.makeupGrade = []
        self.isMakeup = 0
    def add(self,cource, adjuster, makeup = 0):
        cource[0] = cource[0].encode('ascii')
        self.academicYear.append(cource[0][1:10])
        self.semester.append(cource[0][-1])

        cource[1] = cource[1].encode('ascii')
        self.courceCode.append(cource[1])
        try:
            cource[2] = cource[2].encode('ascii')
        except:
            cource.insert(2,'###########'.encode('ascii'))
            adjuster = adjuster - 1      # if init cource[2] is NULL,there can't encode as 'ascii'

        self.courceNumber.append(cource[2])
        self.courceName.append(cource[3])

        self.courceType.append(cource[4][:-2])

        self.courceCredit.append(cource[4].encode('utf-8')[-1])


        #6,+8

        if (makeup):
            self.isMakeup = 1
            self.makeupGrade.append(cource[6].encode('utf-8').strip())


        try:
            self.courceGrade.append(int(cource[5]))
            self.courceFinal.append(int(cource[6 + makeup]))
        except:
            if (re.findall(u'未通过',cource[5]) != None):
                self.courceGrade.append(0)
                self.courceFinal.append(0)
            elif (re.findall(u'通过',cource[5]) != None):
                self.courceGrade.append(100)
                self.courceFinal.append(100)
            else:
                print "发现不知名的成绩.."

        if (self.courceGrade[self.count] >= 85):
            self.courceGPA.append(4)
        elif (self.courceGrade[self.count] < 60):
            self.courceGPA.append(1)
        else:
            self.courceGPA.append(4 - (85 - self.courceGrade[self.count]) * 0.1)



        self.count += 1
        return adjuster


    def printCources(self):
        for i in xrange(0,self.count, 1):
            print self.academicYear[i],
            print "第",
            print self.semester[i],
            print "学期",
            # print self.courceCode[i],
            # print self.courceNumber[i],
            # print self.courceType,
            print " --> ",
            print self.courceName[i].encode('utf-8'),
            print self.courceType[i].encode('utf-8')
            # print "-------------------------------------------> ",
            print "----------------------> ",
            print self.courceCredit[i],
            print "学分",
            print "总评",
            print self.courceGrade[i],
            print "最终",
            print self.courceFinal[i],
            print "单科绩点",self.courceGPA[i],
            if (self.isMakeup == 1 and self.makeupGrade[i] != '--'):
                print "补考成绩 ",
                print self.makeupGrade[i]
            else:
                print ""



class GradeAnalyzer:

    def __init__(self,html):
        self.soup = BeautifulSoup(html)
        '''
            griddata-even + griddata-odd 交叉排列
            分别放在list内,
            其中even最后一个是在校汇总,odd最后一个是统计时间

        '''
        self.termData = TermStruct()
        self.courcesData = Courcestruct()

    def printTotal(self):


        self.griddata_even = self.soup.select(".griddata-even")
        self.griddata_odd  = self.soup.select(".griddata-odd")

        self.griddata = []
        for i in xrange(0, len(self.griddata_even) - 1, 1):
            self.griddata.append(self.griddata_even[i].get_text().encode('ascii'))
            for j in xrange(0, len(self.griddata_odd) - 1, 1):
                self.griddata.append(self.griddata_odd[i].get_text().encode('ascii'))

        for i in xrange(0,len(self.griddata), 1):
            self.griddata[i] = self.griddata[i].strip('\n').split('\n')
            self.termData.addList(self.griddata[i])

        self.termData.printAll()

        self.griddata = []
        if (len(self.griddata_even) > len(self.griddata_odd)):
            ### 1,3,5,7 term
            self.griddata.append(self.griddata_odd[-1].get_text().encode('ascii','ignore').strip('\n').split('\n'))
            self.griddata.append(self.griddata_even[-1].get_text().encode('ascii','ignore').strip('\n').strip(':').split('\n'))
        else:
            ### 2,4,6,8 term
            self.griddata.append(self.griddata_even[-1].get_text().encode('ascii','ignore').strip('\n').split('\n'))
            self.griddata.append(self.griddata_odd[-1].get_text().encode('ascii','ignore').strip('\n').strip(':').split('\n'))

        self.termData.addFinal(self.griddata[0],self.griddata[1])
        self.termData.printFinal()

    def printCources(self):
        self.total = self.termData.getCourseNumber()
        self.gridCources = self.soup.find(id = "grid21344342991_data").get_text()
        temp = re.findall('(?u).*',self.gridCources)
        tempA = []
        for i in xrange(0,len(temp),1):
            if (temp[i] == ''):
                continue
            else:
                tempA.append(temp[i])

        isMakeup = judgeExistMakeupGrade(tempA)
        # print tempA
        # for i in tempA:
        #     print i

        # for i in xrange(0,len(tempA),7 + isMakeup): #there is a bug to repair,I need set a adjuster
        #     print i
        #     i = self.courcesData.add(tempA[i:i + 7 + isMakeup],i,isMakeup)
        #     print i
        # self.courcesData.printCources()

        i = 0
        while(i < len(tempA)):
            # print i
            i = self.courcesData.add(tempA[i:i + 7 + isMakeup],i,isMakeup)
            # print i
            i += (7 + isMakeup)
        self.courcesData.printCources()

class UESTC:

    def __init__(self,username = 0,password = 0):
        self.loginURL = "https://uis.uestc.edu.cn/amserver/UI/Login"
        self.urlEAS = "http://eams.uestc.edu.cn/eams/home.action"
        self.urlCurriculumManager = "http://eams.uestc.edu.cn/eams/home!childmenus.action?menu.id=844"
        self.urlMygrade = "http://eams.uestc.edu.cn/eams/teach/grade/course/person!historyCourseGrade.action?projectType=MAJOR"
        self.urlCources = "http://eams.uestc.edu.cn/eams/courseTableForStd!courseTable.action"
        self.cookies = cookielib.CookieJar()
        if (username != 0):
            self.__inputUserName__ = username
            self.__inputPassWord__ = password
        else:
            self.__inputUserName__ = raw_input("UserName:")
            self.__inputPassWord__ = raw_input("PassWord:")
        self.postData = urllib.urlencode(
            {
                'IDToken0':'',
                'IDToken1':self.__inputUserName__,
                'IDToken2':self.__inputPassWord__,
                'IDButton':'Submit',
                'goto':'aHR0cDovL3BvcnRhbC51ZXN0Yy5lZHUuY24vbG9naW4ucG9ydGFs',
                'encoded':'true',
                'gx_charset':'UTF-8'
            })
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookies))




    def getIndex(self,getter = False):     # login index page
        self.request = urllib2.Request(
            url = self.loginURL,
            data = self.postData)
        self.result = self.opener.open(self.request)
        if (getter):
            return self.result.read()


    def getEAS(self,getter = False):    #  click educational administration system
        request = urllib2.Request(url = self.urlEAS)
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookies))
        result = self.opener.open(request)
        if (getter):
            return result.read()

    def getCurriculumManager(self,getter = False):  # table
        request = urllib2.Request(url = self.urlCurriculumManager)
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookies))
        result = self.opener.open(request)
        if (getter):
            return result.read()

    def getMyGrade(self,getter = False):
        request = urllib2.Request(url = self.urlMygrade)
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookies))
        result = self.opener.open(request)
        if (getter):
            return result.read()

    def getCources(self,getter = False):
        postData = urllib.urlencode(
            {
                'ignoreHead':'1',
                'setting.kind':'std',
                'startWeek':'1',
                'project.id':'1',
                'semester.id':'43',# 43:2015-2016.1 43:2014-2015.6
                'ids':'133737'
            }
        )
        request = urllib2.Request(
            url = self.urlCources,
            data = postData
        )
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookies))
        result = self.opener.open(request)
        if (getter):
            return result.read()



def init(username,password):
    old = sys.stdout
    fileNew = 'new'+username+'.txt'
    f = open(fileNew,'w')
    sys.stdout = f

    uestc = UESTC(username,password)
    uestc.getIndex()
    uestc.getEAS()
    # uestc.getCurriculumManager()

    grade = GradeAnalyzer(uestc.getMyGrade(True))
    grade.printTotal()
    grade.printCources()

    sys.stdout = old
    f.close()

if __name__ == '__main__':
    uestc = UESTC()
    uestc.getIndex()
    uestc.getEAS()


    grade = GradeAnalyzer(uestc.getMyGrade(True))

    grade.printTotal()
    grade.printCources()


###BUG:  the cource[2] may not have