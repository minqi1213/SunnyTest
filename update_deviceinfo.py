#coding=utf-8

import time

import hashlib
import requests
import json
import urllib2

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

def check_status(appkey, task_id):
    timestamp = int(time.time() * 1000 )
    method = 'POST'
    url = 'http://msg.umeng.com/api/status'
    params = {'appkey': appkey,
              'timestamp': timestamp,
              'task_id': task_id,
    }
    post_body = json.dumps(params)
    print post_body
    sign = md5('%s%s%s%s' % (method,url,post_body,app_master_secret))
    try:
        r = urllib2.urlopen(url + '?sign='+sign, data=post_body)
        status = json.loads(r.read())
    except urllib2.HTTPError,e:
        print e.reason,e.read()
    except urllib2.URLError,e:
        print e.reason
    return status

if __name__ == '__main__':
    appkey = '572c03e667e58eebb900296a'
    app_master_secret = '8apsguekwhqtenzrykmjotum5cxtedqt'
    custom_content = json.loads('{"action_type":7}')
    device_token = 'Atv003d_gM4n70qSvIpqXLgzPvawikih8EoHA1Ql2PcB,AhFtEA2Dxekaq-v4GwpzreHgWtNYrokgk3UPpbcnTE9W'

    task_id = push_broadcast(appkey, app_master_secret, device_token, custom_content)
    print task_id
#     print check_status(appkey, "us20790146252096081800")
