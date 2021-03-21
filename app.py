from flask import Flask,request,flash
from flask import render_template
from flaskext.mysql import MySQL
from pyunit_calendar import BatchCalendar
import random
# from mysql import mysql
# from flaskext.mysql import MySQL

mysql = MySQL()
app=Flask(__name__)
app.secret_key = 'super secret key'

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'shanyang'
app.config['MYSQL_DATABASE_DB'] = 'wenzhou'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
conn = mysql.connect()
# cursor =conn.cursor()

@app.route('/')
def index():
    return 'welcome to my webpage!'

@app.route('/add/', methods=['GET', 'POST'])
# @app.route('/hello/name')
def hello(name=None,item=None):
    genders = ['男','女']
    if (request.method == "POST") and (request.form['year']!=None):
        details = request.form
        year = details['year']
        month = details['month']
        day = details['day']
        date = year + '年' + month + '月' + day + '日'
        bc=BatchCalendar()
        sc = bc.td_to_sc(date)
        item = list()
        print(sc)
        item.append(sc[0].split('年',1)[0])
        item.append(sc[0].split('年',1)[1].split('月',1)[0])
        item.append(sc[0].split('年',1)[1].split('月',1)[1].split('日')[0])
        item.append(year)
        item.append(month)
        item.append(day)
        print(item)
        return render_template('add.html',item=item)
    elif (request.method == "POST"):
        details = request.form
        print(details)
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

        cur = conn.cursor()
        sql = "INSERT INTO `people`(`nameid`,`surname`,`first_name`,`gender`,`yearofbirth`,`yearofdeath`,`hometown`,`residence`,`zi`,`hao`,`gongming`)  VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cur.execute(sql, (veri_res, firstName, lastName,gender, yearofbirth, yearofdeath, ht, residence, zi, hao, gongming))
        conn.commit()
        cur.close()
        flash('You were successfully logged in')
        # flash(u'Invalid password provided', 'error')
        return render_template('add.html')
    return render_template('add.html', data=genders, item=None)

@app.route('/data')
def data(data=None):
    return render_template('data.html',data=data)

@app.route('/search') 
def search():
    page = request.args.get('page')
    if not page or int(page) == 0:
        page = 1
    keyword = request.args.get('keyword')
    items = getItems(conn, page, keyword)
    page_range = range(int(page) - 3, int(page) + 2)
    if int(page) < 4:
        page_range = range(1, int(page) + 4)
    return render_template('search.html', items=items,page=int(page),prange = page_range)

@app.route('/edit') 
def edit():
    item=['1','1','1','1']
    return render_template('edit.html',item=item)
         
def getItems(self,page,keyword=None):
    sql = "select * from people"
    if keyword:
        sql = sql + " where gender like '%" + keyword + "%'"
    start = (int(page) - 1) * 10
    sql = sql + " limit " + str(start) + ",13"
    cursor =self.cursor()
    cursor.execute(sql)
    items = cursor.fetchall()
    return items

if __name__=="__main__":
    app.run(port=5000,host="127.0.0.1",debug=True)