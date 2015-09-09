
import xlrd
import sqlite3

class DB:
    def __init__(self):
        self.cx = sqlite3.connect('dorm.db')
        self.cu = self.cx.cursor()
        sql = "CREATE TABLE IF NOT EXISTS `bedInfo` (`_id_` integer primary key autoincrement, `name` text(128), `student_code` varchar(128), `sex` text(8), `college` text(128), `major` text(128), `grade` varchar(28), `class` varchar(128), `campus` text(256), `dorm_group` text(128), `dorm_build_number` text(128), `dorm_floor` text(128), `room` varchar(8), `standard` varchar(20), `bed` varchar(8))"
        self.cu.execute(sql)
        self.cx.commit()
    def add(self,stu):
        values = "'" + str(stu[0]) + "'," + "'" + str(stu[1]) + "'," + "'" + str(stu[2]) + "'," + "'" + str(stu[3]) + "'," + "'" + str(stu[4]) + "'," + "'" + str(stu[5] ) + "'," + "'" + str(stu[6]) + "'," + "'" + str(stu[7]) + "'," + "'" + str(stu[8]) + "'," + "'" + str(stu[9]) + "'," + "'" + str(stu[10]) + "'," + "'" + str(stu[11]) + "'," + "'" + str(stu[12]) + "'," + "'" + str(stu[13]) + "'," + "'" + str(stu[14] + "'")
        sql = "INSERT INTO bedInfo(_id_,name,student_code,sex,college,major,grade,class,campus,dorm_group,dorm_build_number,dorm_floor,room,standard,bed) VALUES (" +values + ")"
        print (sql)
        self.cu.execute(sql)
        self.cx.commit()

record = []
def init():
    xlsfile = xlrd.open_workbook("dorm.xls")

    try:
        table = xlsfile.sheets()[0]
        i = 0
        while(1):
            record.append(table.row_values(i))
            i = i + 1
    except:
        print (i)


db = DB()
init()

for i in range(1,len(record),1):
    db.add(record[i])