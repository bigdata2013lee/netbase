#coding=utf-8
###########################################################################
#       
#
#此软件版权为深圳商之杰科技有限公司所有,更多信息请访问www.netbase.asia
#
#
###########################################################################
from products.netUtils.xutils import nbPath as _p

__doc__ = """
接口组件配置获取
"""
import os
import commands
from products.dataCollector.plugins.CollectorPlugin import IpmiPlugin

class FanRpmMap(IpmiPlugin):
    
    maptype = "FanRpmMap" 
    compname = "os"
    command = ''
    def process(self,obj,log):
        """
                获取数据并对数据进行处理
        """
        errMsg=""
        datamaps=[]
        try:
            rs=commands.getoutput("exec %s/libexec/ipmi-sensors -h %s -u %s -p %s -g Fan"%(
                                                    _p(),obj.ipmiConfig.get("netIpmiIp"),
                                                    obj.ipmiConfig.get("netIpmiUserName"),obj.ipmiConfig.get("netIpmiPassword")))
            for sdr in rs.splitlines():
                fanRpms=sdr.split(":")
                if not len(fanRpms)==4:continue
                fanId,uname,fanstatus,letuname=self.parseFan(fanRpms)
                datamaps.append(dict(fanId=fanId,uname=uname,fanstatus=fanstatus,letuname=letuname))
        except OSError,error:
            errMsg="无法获取数据,请检查IPMI配置是否正确!"
            log.error(error)
        return errMsg,datamaps
    
    def parseFan(self,fanRpms):
        """
                解析风扇的返回值
        """
        fanId=fanRpms[0].strip()
        letuname=fanRpms[1].rsplit(" ",1)[0].strip()
        fanstatus=fanRpms[3].strip()[1:-1]
        return fanId,letuname,fanstatus,letuname