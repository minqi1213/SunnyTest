#! /usr/bin/python
# -*- coding: utf-8 -*- 

HOST = '101.200.179.166'
PORT = 3306
USER = 'root'
PASSWORD = '123456'
DBNAME = 'SunnyTest'
CHARSET = 'utf8'

def connect():
    try:
        import MySQLdb
    except ImportError, e:
        print e 
        return None
    try:
        cxn = MySQLdb.connect(host=HOST, user=USER, passwd=PASSWORD,port=PORT,db=DBNAME,charset=CHARSET)
        print cxn
        return cxn
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        
# 插入操作
def insert_one(cur,sql,value):
    res =  cur.execute(sql ,value)
    # 插入成功，res 返回值为1 
    if  1 != res :
        print 'failed'
    else:
        print 'success'
        
getRC = lambda cur: cur.rowcount if hasattr(cur,'rowcount')  else -1

# 更新操作
def update(cur,sql):
    cur.execute(sql)
    return getRC(cur)

# 删除操作
def delete(cur,sql,params):
    cur.execute(sql,params)
    return getRC(cur)

# 只获取一条记录，返回的是一个元组

def fetch_one(cur,sql):
    count = cur.execute(sql)
    #print count
    result = cur.fetchone();  
    return result

# 获取多条数据；返回的是二维元组；
def fetch_all(cur,sql):
    count = cur.execute(sql)
    #print count
    results = cur.fetchall();  
    '''
    print results
    for r in results:  
        print r  
    '''
    return results

# 提交的完成操作
def finish(cxn):
    cxn.commit()
    cxn.close()
