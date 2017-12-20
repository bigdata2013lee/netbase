#!/usr/bin/python
#coding=utf-8
import time
import commands
import logging
from products.netUtils.xutils import nbPath as _p
log = logging.getLogger("netIpmi")
from products.dataCollector.redisManager import RedisManager

exec_ipmitool=r"exec %s/libexec/ipmitool " %_p()

class BootIpmiTask(RedisManager):
    """
        功能:ipmi类,用于开关机或者获取设备电源状态
        使用于支持IPMI的设备并需做先关的配置
        硬重启有可能会造成硬盘的raid丢失或者数据的丢失,所以谨慎使用
        作者:wl
        时间:2013.11.12
    """
        
    def __init__(self,cuid,uid,ip,username,password,title,componentType):
        """
                初始化
        """
        self.ip=ip
        self.uid=uid
        self.cuid=cuid
        self.title=title
        self.username=username
        self.password=password
        self.componentType=componentType

    def powerStatus(self):
        """
                电源状态
        """
        try:
            rs=commands.getoutput(exec_ipmitool + " -I lan -H %s -U %s -P '%s' power status "%(self.ip,self.username,self.password))
            if rs.find("Chassis Power is on")>=0:
                return "up"
            return "down"
        except OSError,error:
            logging.error(error)
        return "unknown"

    def powerOn(self):
        """
                硬开机
        """
        try:
            rs=commands.getoutput(exec_ipmitool + " -I lan -H %s -U %s -P '%s' power on "%(self.ip,self.username,self.password))
            print "rs:", rs
            if rs.find(": Up/On")>=0:
                self.createEvent("%s远程开机成功!"%self.ip,2)
                return "远程开机成功!"
        except OSError,error:
            logging.error(error)
        self.createEvent("%s远程开机失败!"%self.ip,4)
        return "warn:远程开机失败,请稍后重试或联系管理人员!"
            

    def softOff(self):
        """
                软关机(相当于按一下关机按钮)
        """
        try:
            rs=commands.getoutput(exec_ipmitool + " -I lan -H %s -U %s -P %s power soft"%(self.ip,self.username,self.password))
            if rs.find(": Soft")>=0:
                self.createEvent("%s远程软关机成功!"%self.ip,2)
                return "远程软关机成功!"
        except OSError,error:
            logging.error(error)
        self.createEvent("%s远程软关机失败!"%self.ip,4)
        return "warn:远程软关机失败,请稍后重试或联系管理人员!"
        
    def powerOff(self):
        """
                硬关机(直接切断电源)
        """
        try:
            rs=commands.getoutput(exec_ipmitool + " -I lan -H %s -U %s -P %s power off"%(self.ip,self.username,self.password))
            if rs.find(": Down/Off")>=0:
                self.createEvent("%s远程硬关机成功!"%self.ip,2)
                return "远程硬关机成功!"
        except OSError,error:
            logging.error(error)
        self.createEvent("%s远程硬关机失败!"%self.ip,4)
        return "warn:远程硬关机失败,请稍后重试或联系管理人员!"
            
    
    def powerReset(self):
        """
                硬重启
        """
        try:
            rs=commands.getoutput(exec_ipmitool + " -I lan -H %s -U %s -P %s   power reset"%(self.ip,self.username,self.password))
            if rs.find(": Reset")>=0:
                self.createEvent("%s远程硬重启成功!"%self.ip,2)
                return "远程硬重启成功!"
        except OSError,error:
            logging.error(error)
        self.createEvent("%s远程硬重启失败!"%self.ip,4)
        return "warn:远程硬重启失败,请稍后重试或联系管理人员!"
        
    def log(self):
        """
                日志
        """
        try:
            rs=commands.getoutput(exec_ipmitool + " -I lan -H %s -U %s -P '%s' sel list"%(self.ip,self.username,self.password))
        except OSError,error:
            logging.error(error)
        return rs
    
    def getAmbientTemp(self):
        """
                获取机箱温度
        """
        try:
            rs=commands.getoutput(exec_ipmitool + " -I lan -H %s -U %s -P '%s' sensor  get 'Ambient Temp'| /bin/grep -i 'Sensor Reading'|/bin/cut -c 26-28"%(self.ip,self.username,self.password))
            return rs
        except OSError,error:
            logging.error(error)
        return "unknown"
    
    def createEvent(self,message,severity):
        """
                生成事件
        """
        data = {
          'moUid':self.uid,
          'title':self.title,
          "componentType":self.componentType,
          "message":"%s %s"%(time.strftime("%Y-%m-%d %H:%M",time.localtime()),message),
          "severity":severity,
          "collector":self.cuid,
          "agent":"netboot"
        }
        self.saveEvent(data)
        

if __name__=="__main__":
    import sys
    startTime=time.time()
    ip,username,password=sys.argv[1:]
    bi=BootIpmiTask(ip,username,password)