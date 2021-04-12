from flask import Flask,request,flash
from flask import render_template
from flaskext.mysql import MySQL
from pyunit_calendar import BatchCalendar
import random
import sql

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

@app.route('/add', methods=['GET', 'POST'])
def add(name=None,item=None):
    genders = ['男','女']
    if (request.method == "POST") and ('year' in request.form):
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
    elif (request.method == "POST" and request.form['fname']!='' and request.form['lname']!=''):
        details = request.form
        print(details)
        sql.addPeople(conn,details)
        # flash(u'Invalid password provided', 'error')
        return render_template('add.html',data=genders,item=None)
    return render_template('add.html', data=genders, item=None)

@app.route('/data')
def data(data=None):
    return render_template('data.html',data=data)

@app.route('/search')   # search item according to keywords
def search():
    page = request.args.get('page')
    if not page or int(page) == 0:
        page = 1
    keyword = request.args.get('keyword')
    items = sql.getItemsByGender(conn, page, keyword)
    page_range = range(int(page) - 3, int(page) + 2)
    if int(page) < 4:
        page_range = range(1, int(page) + 4)
    return render_template('search.html', items=items,page=int(page),prange = page_range)

@app.route('/edit') 
@app.route('/edit/<id>', methods=['GET','POST'])
def edit(id=None):
    if (request.method == 'GET') and (id!=None):  # read data from database
        items = sql.getItemsById(conn, id)
        return render_template('edit.html',item=items)
    if (request.method == 'POST'):  # edit data
        # get the new parameters
        return render_template('edit.html',item=items)
    return render_template('edit.html',item=None)

@app.route('/index') 
def homepage():
    return render_template('homepage.html')

@app.route('/delete') 
@app.route('/delete/<id>', methods=['GET','POST'])
def delete(id=None):
    if (request.method == 'GET') and (id!=None):  # read data from database
        items = sql.delete(conn, id)
    return search()

@app.route('/parent', methods=['GET','POST'])
def parent():
    if (request.method == 'POST'):
        details = request.form
        print(details)
        sql.parent(conn,details)
    return render_template('parent.html')

if __name__=="__main__":
    app.run(port=5000,host="127.0.0.1",debug=True)