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

def getItemsByName(self,page,keyword=None):
    sql = "select * from people"
    if keyword:
        sql = sql + " where concat(`surname`,`first_name`) = %s"
    start = (int(page) - 1) * 10
    sql = sql + " limit " + str(start) + ",13"
    cursor =self.cursor()
    cursor.execute(sql,(keyword))
    items = cursor.fetchall()
    return items

def getItemsByZibei(self,page,keyword=None):
    sql = "select * from people"
    if keyword:
        sql = sql + " where zibei = %s"
    start = (int(page) - 1) * 10
    sql = sql + " limit " + str(start) + ",13"
    cursor =self.cursor()
    cursor.execute(sql,(keyword))
    items = cursor.fetchall()
    return items

def getItemsById(self, keyword=None):
    sql = "select * from people"
    sql = sql + " where nameid = " + keyword
    cursor =self.cursor()
    cursor.execute(sql)
    items = cursor.fetchone()
    return items

def delete(self, keyword=None):
    sql = "delete from people"
    sql = sql + " where nameid = " + keyword
    cursor =self.cursor()
    cursor.execute(sql)
    items = cursor.fetchone()
    return items

def parent(self, keyword=None):
    fatherid = keyword['father1']
    fathername = keyword['father2']
    offspringid = keyword['son1']
    offspringname = keyword['son2']
    sql = "insert into `father`(`offspringid`,`offspringname`,`fatherid`,`fathername`) values(%s,%s,%s,%s)"
    cursor = self.cursor()
    cursor.execute(sql,(offspringid,offspringname,fatherid,fathername))
    self.commit()
    cursor.close()
    flash('成功')

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
    fangxi = details['fangxi']
    zibei = details['zibei']
    wife = details['wife']
    daughter = details['daughter']

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
    sql = "INSERT INTO `people`(`nameid`,`surname`,`first_name`,`gender`,`yearofbirth`,`yearofdeath`,`hometown`,`residence`,`zi`,`hao`,`gongming`,`fangxi`,`zibei`,`wife`,`daughter`)  VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    cur.execute(sql, (veri_res, firstName, lastName,gender, yearofbirth, yearofdeath, ht, residence, zi, hao, gongming,fangxi,zibei,wife,daughter))
    self.commit()
    cur.close()
    flash('成功')

def update(self,details=None,id=None):
    zi = details['zi']
    hao = details['hao']
    ht = details['hometown']
    residence = details['residence']
    gongming = details['gongming']
    fangxi = details['fangxi']
    zibei = details['zibei']
    wife = details['wife']
    daughter = details['daughter']
    cur = self.cursor()
    sql = "UPDATE people SET hometown=%s, residence=%s, zi=%s,hao=%s,gongming=%s,fangxi=%s,zibei=%s,wife=%s,daughter=%s WHERE nameid = %s"
    cur.execute(sql, (ht, residence, zi, hao, gongming,fangxi,zibei,wife,daughter,id))
    self.commit()
    cur.close()
    flash('成功')