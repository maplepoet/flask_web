import app
import random
from flask import flash

def getItemsByGender(self,page,keyword=None):
    sql = "select * from people"
    if keyword:
        sql = sql + " where gender like '%" + keyword + "%'"
    start = (int(page) - 1) * 10
    sql = sql + " limit " + str(start) + ",13"
    cursor =self.cursor()
    cursor.execute(sql)
    items = cursor.fetchall()
    return items

def getItemsById(self, keyword=None):
    sql = "select * from people"
    sql = sql + " where nameid = " + keyword
    cursor =self.cursor()
    cursor.execute(sql)
    items = cursor.fetchone()
    return items

def addPeople(self, details=None):
    firstName = details['fname']
    lastName = details['lname']
    gender = details.get('gender')
    if (details['yearofbirth']==''):
        yearofbirth = None
    else:
        yearofbirth = details['yearofbirth']
    if (details['yearofdeath']==''):
        yearofdeath = None
    else:
        yearofdeath = details['yearofdeath']
    zi = details['zi']
    hao = details['hao']
    ht = details['hometown']
    residence = details['residence']
    gongming = details['gongming']

    # calculate the unique id (according to the gender)
    veri_res=''
    list_num = [1,2,3,4,5,6,7,8,9,0]
    veri_num = random.sample(list_num,4)
    for i in range(4):
        veri_res+=str(veri_num[i])
    veri_res += yearofbirth
    if (gender == '男'):
        veri_res+='1'
    elif (gender == '女'):
        veri_res+='0'

    cur = self.cursor()
    sql = "INSERT INTO `people`(`nameid`,`surname`,`first_name`,`gender`,`yearofbirth`,`yearofdeath`,`hometown`,`residence`,`zi`,`hao`,`gongming`)  VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    cur.execute(sql, (veri_res, firstName, lastName,gender, yearofbirth, yearofdeath, ht, residence, zi, hao, gongming))
    self.commit()
    cur.close()
    flash('成功')