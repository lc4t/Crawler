import simplejson
import json
import add2db


def makedict(stu):
    result = {}
    result['majorName'] = stu['majorName']
    result['exitstate'] = stu['exitstate']
    result['examNum'] = stu['examNum']
    result['changeDate'] = stu['changeDate']
    result['tfyy'] = stu['tfyy']
    result['yfloorName'] = stu['yfloorName']
    result['gradeName'] = stu['gradeName']
    result['familyAddress'] = stu['familyAddress']
    result['phone'] = stu['phone']
    result['email'] = stu['email']
    result['id'] = stu['id']
    result['floorName'] = stu['floorName']
    result['enterDate'] = stu['enterDate']
    result['bol'] = stu['bol']
    result['opName'] = stu['opName']
    result['occupancyDate'] = stu['occupancyDate']
    result['remark'] = stu['remark']
    result['tuidate'] = stu['tuidate']
    result['name'] = stu['name']
    result['collegeName'] = stu['collegeName']
    result['bedName'] = stu['bedName']
    result['lodgeState'] = stu['lodgeState']
    result['jsr'] = stu['jsr']
    result['yareaName'] = stu['yareaName']
    result['returnDate'] = stu['returnDate']
    result['graduateDate'] = stu['graduateDate']
    result['xz'] = stu['xz']
    result['className'] = stu['className']
    result['position'] = stu['position']
    result['gender'] = stu['gender']
    result['ybedName'] = stu['ybedName']
    result['brithday'] = stu['brithday']
    result['jjlxr'] = stu['jjlxr']
    result['identity'] = stu['identity']
    result['stuNum'] = stu['stuNum']
    result['yfeebz'] = stu['yfeebz']
    result['buildName'] = stu['buildName']
    result['userName'] = stu['userName']
    result['roomName'] = stu['roomName']
    result['graduatedCollege'] = stu['graduatedCollege']
    result['jjlxrphone'] = stu['jjlxrphone']
    result['stutype'] = stu['stutype']
    result['bedIdBeforeStay'] = stu['bedIdBeforeStay']
    result['exitMoney'] = stu['exitMoney']
    result['sex'] = stu['sex']
    result['yroomName'] = stu['yroomName']
    
    result['feebz'] = stu['feebz']
    result['noDocument'] = stu['noDocument']
    result['photo'] = stu['photo']
    result['memberType'] = stu['memberType']
    result['cwbh'] = stu['cwbh']
    result['areaName'] = stu['areaName']
    result['memberids'] = stu['memberids']
    result['yuanYin'] = stu['yuanYin']
    result['available'] = stu['available']
    result['ybuildName'] = stu['ybuildName']


    try:
        result['politics_dictType'] = stu['studentType']['dictType']
        result['politics_available'] = stu['studentType']['available']
        result['politics_dictName'] = stu['studentType']['dictName']
        result['politics_dictCode'] = stu['studentType']['dictCode']
    except:
        result['politics_dictType'] = ''
        result['politics_available'] = ''
        result['politics_dictName'] = ''
        result['politics_dictCode'] = ''

    try:
        result['studentType_remark'] = stu['studentType']['remark']
        result['studentType_available'] = stu['studentType']['available']
        result['studentType_id'] = stu['studentType']['id']
        result['studentType_typeName'] = stu['studentType']['typeName']
    except:
        result['studentType_remark'] = ''
        result['studentType_available'] = ''
        result['studentType_id'] = ''
        result['studentType_typeName'] = ''
    try:
        result['major_majorName'] = stu['major']['majorName']
        result['major_remark'] = stu['major']['remark']
        result['major_available'] = stu['major']['available']
        result['major_id'] = stu['major']['id']
        result['major_mcode'] = stu['major']['mcode']
    except:
        result['major_majorName'] = ''
        result['major_remark'] = ''
        result['major_available'] = ''
        result['major_id'] = ''
        result['major_mcode'] = ''

    try:
        result['nationId_available'] = stu['nationId']['available']
        result['nationId_adictName'] = stu['nationId']['adictName']
        result['nationId_dictCode'] = stu['nationId']['dictCode']
        result['nationId_dictType'] = stu['nationId']['dictType']
    except:
        result['nationId_available'] = ''
        result['nationId_adictName'] = ''
        result['nationId_dictCode'] = ''
        result['nationId_dictType'] = ''

    try:
        result['grade_remark'] = stu['grade']['remark']
        result['grade_available'] = stu['grade']['available']
        result['grade_gradeName'] = stu['grade']['gradeName']
        result['grade_id'] = stu['grade']['id']
    except:
        result['grade_remark'] = ''
        result['grade_available'] = ''
        result['grade_gradeName'] = ''
        result['grade_id'] = ''

    try:
        result['schoolClass_remark'] = stu['schoolClass']['remark']
        result['schoolClass_available'] = stu['schoolClass']['available']
        result['schoolClass_className'] = stu['schoolClass']['className']
        result['schoolClass_id'] = stu['schoolClass']['id']
    except:
        result['schoolClass_remark'] = ''
        result['schoolClass_available'] = ''
        result['schoolClass_className'] = ''
        result['schoolClass_id'] = ''

    try:
        result['nativeId_dictCode'] = stu['nativeId']['dictCode']
        result['nativeId_available'] = stu['nativeId']['available']
        result['nativeId_dictName'] = stu['nativeId']['dictName']
        result['nativeId_dictType'] = stu['nativeId']['dictType']
    except:
        result['nativeId_dictCode'] = ''
        result['nativeId_available'] = ''
        result['nativeId_dictName'] = ''
        result['nativeId_dictType'] = ''

    try:
        result['college_ccode'] = stu['college']['ccode']
        result['college_parent'] = stu['college']['parent']
        result['college_remark'] = stu['college']['remark']
        result['college_parentName'] = stu['college']['parentName']
        result['college_available'] = stu['college']['available']
        result['college_collegeName'] = stu['college']['collegeName']
        result['college_id'] = stu['college']['id']
    except:
        result['college_ccode'] = ''
        result['college_parent'] = ''
        result['college_remark'] = ''
        result['college_parentName'] = ''
        result['college_available'] = ''
        result['college_collegeName'] = ''
        result['college_id'] = ''


    return result



data = []
for i in range(0,86,1):

    print (i)
    jsondata = open('json/'+str(i)+'.json','r').read()
    jsondata = jsondata.replace('"',"'")  ##Isma" on 9.json is not match
    onestu = eval(jsondata)

    onestu = onestu['results']
    for j in range(0,len(onestu),1):
        data.append(makedict(onestu[j]))

db = add2db.DB()

for i in range(0,len(data),1):
    db.add(data[i])
    print (str(i) + '/85387')



