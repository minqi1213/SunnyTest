#coding=utf-8

import time
import hashlib
import requests
import json
import urllib2
import sys, getopt
from getDevicesToken import *

appkey = '572c03e667e58eebb900296a'
app_master_secret = '8apsguekwhqtenzrykmjotum5cxtedqt'
device_token =  getDevicesToken()
custom_content = '123456'

def Usage():
    print 'PyTest.py usage:'
    print '-h,--help: print help message.'
    print '-v, --version: print script version'
    print '-t, --action_type: input an action type'

def Version():
    print 'main.py 1.0.0.0.1'

def md5(s):
    m = hashlib.md5(s)
    return m.hexdigest()

def push_broadcast(appkey, app_master_secret, device_token, custom_content):
    timestamp = int(time.time() * 1000 )
    method = 'POST'
    url = 'http://msg.umeng.com/api/send'
    params = {'appkey': appkey,
              'timestamp': timestamp,
              'device_tokens': device_token,
              'type': 'broadcast',
              'payload': {'body': {
                                   'custom':custom_content},
                          'display_type': 'message'
              }
    }
    post_body = json.dumps(params)
    print post_body
    sign = md5('%s%s%s%s' % (method,url,post_body,app_master_secret))
    try:
        r = urllib2.urlopen(url + '?sign='+sign, data=post_body)
        taskID = json.loads(r.read())['data']['task_id']
    except urllib2.HTTPError,e:
        print e.reason,e.read()
    except urllib2.URLError,e:
        print e.reason
    return taskID

def OutPut(args):
    custom_content = json.loads('{"action_type":%s,\
                                  "url":"BaiduMap.apk",\
                                  "application":"BaiduMap",\
                                  "package_name":"com.baidu.BaiduMap",\
                                  "application":"BaiduMap",\
                                  "startcmd":"am start -n com.baidu.BaiduMap/com.baidu.baidumaps.WelcomeScreen",\
                                  "stopcmd":"am force-stop com.baidu.BaiduMap",\
                                  "sql":true}'%args)
    task_id = push_broadcast(appkey, app_master_secret, device_token, custom_content)
    print task_id
    print 'Hello, %s'%args

def main(argv):

    try:
        opts, args = getopt.getopt(argv[1:], 'hvt:', ['type='])
    except getopt.GetoptError, err:
        print str(err)
        Usage()
        sys.exit(2)
    for o, a in opts:
        if o in ('-h', '--help'):
            Usage()
            sys.exit(1)
        elif o in ('-v', '--version'):
            Version()
            sys.exit(0)
        elif o in ('-t', '--type'):
            OutPut(a)
            sys.exit(0)
        else:
            print 'unhandled option'
            sys.exit(3)


if __name__ == "__main__":
    main(sys.argv)
