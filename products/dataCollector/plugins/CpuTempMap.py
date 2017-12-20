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

class CpuTempMap(IpmiPlugin):
    
    maptype = "CpuTempMap" 
    compname = "os"
    command = ''
    def process(self,obj,log):
        """
                获取数据并对数据进行处理
        """
        errMsg=""
        datamaps=[]
        try:
            rs=commands.getoutput("exec %s/libexec/ipmi-sensors -h %s -u %s -p %s -g Temperature"%(
                                                    _p(),obj.ipmiConfig.get("netIpmiIp"),
                                                    obj.ipmiConfig.get("netIpmiUserName"),obj.ipmiConfig.get("netIpmiPassword")))
            for sdr in rs.splitlines():
                if not sdr.find("Temp")>=0:continue
                cpuTemps=sdr.split(":")
                if not len(cpuTemps)==4:continue
                tempId=cpuTemps[0].strip()
                tempuname=cpuTemps[1].rsplit(" ",1)[0].strip()
                cpustatus=cpuTemps[3].strip()[1:-1]
                uname=tempuname[:-5].replace(" ","")
                if tempuname.replace(" ","")=="Temp":uname="Temp%s"%(str(tempId))
                cpuValue=dict(tempId=tempId,
                              uname=uname,
                              tempuname=tempuname,
                              cpustatus=cpustatus)
                datamaps.append(cpuValue)
        except OSError,error:
            errMsg="无法获取数据,请检查IPMI配置是否正确!"
            log.error(error)
        return errMsg,datamaps