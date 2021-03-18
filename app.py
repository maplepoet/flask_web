from flask import Flask,request
from flask import render_template
from flaskext.mysql import MySQL
# from mysql import mysql
# from flaskext.mysql import MySQL

mysql = MySQL()
app=Flask(__name__)

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

@app.route('/hello/')
@app.route('/hello/name')
def hello(name=None):
    return render_template('hello.html', name=name)

@app.route('/data')
def data(data=None):
    return render_template('data.html',data=data)

@app.route('/index') 
def name():
    page = request.args.get('page')
    if not page or int(page) == 0:
        page = 1
    keyword = request.args.get('keyword')
    items = getItems(conn, page, keyword)
    page_range = range(int(page) - 3, int(page) + 2)
    if int(page) < 4:
        page_range = range(1, int(page) + 4)
    return render_template('index.html', items=items,page=int(page),prange = page_range)
         
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