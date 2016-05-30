#coding=utf-8
from MysqlHelper import *
import MysqlHelper
'''
Created on 2016年5月25日

@author: mario
'''

class CPUAndMemory:
    def __init__(self, fileName, saveFileName, packageName, appName, deviceModel):
        print '***open***'
        self.fileName = fileName
        self.saveFileName = saveFileName
        self.packageName = packageName
        self.appName = appName
        self.deviceModel = deviceModel
        self.file = open(fileName)
        self.infofile = open(saveFileName, 'w')
        
    def __del__(self):
        print "***close***"
        self.file.close()
        self.infofile.close()
        
    def getCpuAndMemory(self):
        list_cpu = []
        list_vss = []
        list_rss = []
        packageName = self.packageName
        saveFileName = self.saveFileName
        file = self.file
        infofile = self.infofile
        line = file.readline()
        while line:
            temp_result = line.replace('\n','').split()
            if temp_result[9] == packageName:
                infofile.writelines(line)
            line = file.readline()
        infofile.close()
        resultFile = open(saveFileName)
        resultLine = resultFile.readline()
        while resultLine:
            temp_line = resultLine.replace('\n','').split()
            list_cpu.append(int(temp_line[2][:-1]))
            list_vss.append(int(temp_line[5][:-1]))
            list_rss.append(int(temp_line[6][:-1]))
            resultLine = resultFile.readline()
        resultFile.close()
        cpumax = max(list_cpu)
        cpuavg = "%.2f" % (float(sum(list_cpu))/len(list_cpu))
        vsizemax = max(list_vss)
        vsizeavg = sum(list_vss)/len(list_vss)
        rssmax = max(list_rss)
        rssavg = sum(list_rss)/len(list_rss)
        print cpumax,cpuavg,vsizemax,vsizeavg,rssmax,rssavg
        sqlquery = ("UPDATE %s " + 
                   "SET cpumax = '%s',cpuavg = '%s'," +
                   "vsizemax = '%s',vsizeavg = '%s'," +
                   "rssmax = '%s',rssavg = '%s' " +
                   "WHERE devicemodel = '%s' ")%(self.appName,cpumax,cpuavg,vsizemax,vsizeavg,rssmax,rssavg,self.deviceModel)
        print sqlquery
        cxn = MysqlHelper.connect()
        cur = cxn.cursor()
        res =  MysqlHelper.update(cur , sqlquery)
        MysqlHelper.finish(cxn)
if __name__ == '__main__':
    f = CPUAndMemory('cpumeminfo.log', 'package.log', 'com.baidu.BaiduMap',"BaiduMap","H60-L01")
    f.getCpuAndMemory()
