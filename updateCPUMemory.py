#coding=utf-8
from ftplib import FTP
import ftplib
import socket
import sys, getopt, datetime,time
from MYFTP import *
from CPUAndMemory import *
'''
Created on 2016年5月23日

@author: mario
'''

FTP_HOST = '101.200.179.166'
FTP_PORT = 21
FTP_TIMEOUT = 30
FTP_USERNAME = 'sunnytest'
FTP_PASSWD = 'Beijing123'

def Usage():
    print 'PyTest.py usage:'
    print '-h,--help: print help message.'
    print '-v, --version: print script version'
    print '-a, --application: input an app name'

def Version():
    print 'main.py 1.0.0.0.1'

def listAllDevices(args):
    list = ''
    try:
        ftp = FTP()
        ftp.connect(FTP_HOST,FTP_PORT,FTP_TIMEOUT) # 连接FTP服务器 
    except (socket.error, socket.gaierror):
        print 'ERROR:cannot reach " %s"' % FTP_HOST 
        return 
    print '***Connected to host "%s"' % FTP_HOST
    try:  
        ftp.login(FTP_USERNAME,FTP_PASSWD) # 登录  
    except ftplib.error_perm:  
        print 'ERROR: cannot login sunnytest'  
        ftp.quit()  
        return  
    print '*** Logged in as "sunnytest"'  
    try:
        print ftp.getwelcome()  # 获得欢迎信息 
        ftp.cwd('/var/ftp/pub/%s'%args)    # 设置FTP路径  
        list = ftp.nlst()       # 获得目录列表  
    except ftplib.error_perm:
        print 'ERROR: cannot change dir /var/ftp/pub/%s'%args
        ftp.quit()
    return list

def downloadLogFile(args, deviceModel):
    list = ''
    try:
        ftp = FTP()
        ftp.connect(FTP_HOST,FTP_PORT,FTP_TIMEOUT) # 连接FTP服务器 
    except (socket.error, socket.gaierror):
        print 'ERROR:cannot reach " %s"' % FTP_HOST 
        return 
    print '***Connected to host "%s"' % FTP_HOST
    try:  
        ftp.login(FTP_USERNAME,FTP_PASSWD) # 登录  
    except ftplib.error_perm:  
        print 'ERROR: cannot login sunnytest'  
        ftp.quit()  
        return  
    print '*** Logged in as "sunnytest"'  
    try:
        ftp.cwd('/var/ftp/pub/%s/%s'%(args, deviceModel))    # 设置FTP路径  
        list = ftp.nlst()       # 获得目录列表  
    except ftplib.error_perm:
        print 'ERROR: cannot change dir /var/ftp/pub/%s/%s'%(args, deviceModel)
        ftp.quit()
    return list

def main(argv):
    rootdir_remote = "/var/ftp/pub"
    try:
        opts, args = getopt.getopt(argv[1:], 'hva:', ['type='])
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
        elif o in ('-a', '--application'):
            f = MYFTP(FTP_HOST, FTP_USERNAME, FTP_PASSWD, rootdir_remote, FTP_PORT)
            f.login()
            for list in listAllDevices(a):
                print "/var/ftp/pub/%s/%s/cpumeminfo.log"%(a,list)
                f.download_file("./cpumeminfo.log", "/var/ftp/pub/%s/%s/cpumeminfo.log"%(a,list))
                result = CPUAndMemory('cpumeminfo.log', 'package.log', 'com.baidu.BaiduMap', a, list)
                result.getCpuAndMemory()
            sys.exit(0)
        else:
            print 'unhandled option'
            sys.exit(3)

if __name__ == '__main__':
    main(sys.argv)
