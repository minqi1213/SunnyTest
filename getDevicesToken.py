#coding=utf-8
import MySQLdb

def getDevicesToken():
    devicesToken = ()
    results = ""
    conn = MySQLdb.connect(
        host = '101.200.179.166',
        port = 3306,
        user = 'root',
        passwd = 'Beijing123',
        db = 'SunnyTest',
        )
    cur = conn.cursor()
    #获取device token
    aa = cur.execute("select devicetoken from devices")
    #print aa
    info = cur.fetchmany(aa)
    for ii in info:
        devicesToken += ii
    cur.close()
    conn.commit()
    conn.close()
    for r in devicesToken:
        results += r + ","
    return results[:-1]

if __name__ == "__main__":
    print getDevicesToken()


