#! /usr/bin/env python
#coding=utf-8
###########################################################################
#
#
#此软件版权为深圳商之杰科技有限公司所有,更多信息请访问www.netbase.asia
#
#
###########################################################################
from products.netPublicModel.collectorLicense import licenseAuth

__doc__ = '''
检测管理端和收集端的连接是否正常
'''
import re,urllib2,pickle
from twisted.internet import reactor
from products.netUtils.deamonBase import DeamonBase
import logging
log = logging.getLogger("netcollector")
from products.netUtils.settings import CollectorSettings


class netcollector(DeamonBase):
    """
       检测管理端和收集端
    """
    collectorCycleInterval = 7200
    collectIp=""

    def updateCollectIp(self,ip):
        """
                更新收集器IP（保存到远程数据库中）
        """
        settings = CollectorSettings.getSettings()
        collUid = settings.get('collector','colUid')
        self.rpyc.getServiceObj().getDataRoot().saveCollector(collUid,ip)


    def setCollectorHost(self):
        """
        远程获取收集器的host（数据库中保存的收集器host的ip）
        """
        settings = CollectorSettings.getSettings()
        collUid = settings.get('collector','colUid')
        self.collectIp = self.rpyc.getServiceObj().getDataRoot().getCollectorHost(collUid)
        
    def getCollectIp(self):
        """
        获取收集器Ip(当前收集器ip地址)
        """
        localip = self.getIp()
        if localip:return localip

    def getIp(self):
        """
        得到Ip(使用于ADSL拨号的情况下获取IP地址)
        """
       
        checkUrls = [
                    "http://www.whereismyip.com",
                    "http://www.ip138.com/ip2city.asp",
                    "http://www.bliao.com/ip.phtml"
        ]
        localip = ""
        for url in checkUrls:
            localip = self.visit(url)
            if localip: return localip

        return localip
    
    def visit(self,url):
        """
        解析IP（如果没有匹配到会抛出group相关异常）
        """
        ip = ""
        try:
            opener = urllib2.urlopen(url)
            ipStr = opener.read()
            ip =  re.search('\d+\.\d+\.\d+\.\d+',ipStr).group(0)
        except:
            pass
        
        return ip

    @licenseAuth
    def start(self):
        """
                开始运行
        """
        print "run netcollector.py"
        localip=self.getCollectIp()
        log.info("localip:%s" %localip)
        if not localip:return
        self.setCollectorHost()
        log.info("host:%s" %self.collectIp)
        if self.collectIp!=localip:
            self.updateCollectIp(localip)
            
    def runCycle(self):
        """
        循环运行
        """
        log.info("开始一个循环周期!")
        self.start()
        reactor.callLater(self.collectorCycleInterval,self.runCycle)

    def run(self): 
        """
        启动reactor
        """
        self.runCycle()
        log.info("开始启动收集器守护进程!")
        reactor.run()

if __name__ == "__main__":
    nis = netcollector()
    nis.run()
