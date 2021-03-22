import app

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