#coding=utf-8
from products.netModel import medata
from products.netModel.middleware.mwBase import MwBase
from products.netUtils.xutils import nbPath as _p
from products.netUtils import xutils
class MwTomcat(MwBase):
    dbCollection = 'MwTomcat'
    def __init__(self, uid=None):
        MwBase.__init__(self)
        
    
    host = medata.plain("host","")
    port = medata.plain("port",8080)
    url = medata.plain("url", "/manager/status")
    ssl =medata.plain("ssl",False)
    httpUsername = medata.plain("httpUsername", "")
    httpPassword = medata.plain("httpPassword", "")
    
    def getManageId(self):
        """
                获取tomcat对象的管理Id
        """
        return self.host
    
    def getCmd(self):
        """
                获取命令
        """
        parts = [_p("/bin/python") ,_p("/products/netCommand/pyexec/check_tomcat.py")]
        if self.host:
            parts.append('-H %s' % self.host)
        if self.port:
            parts.append('-p %s' % self.port)
        if self.url:
            parts.append("-u %s" % self.url)
        if self.httpUsername:
            parts.append('--username %s' % self.httpUsername)
        if self.httpPassword:
            parts.append('--password %s' % self.httpPassword)
        cmd = ' '.join(parts)
        return cmd
    
    
    
    
    
    def getConnCount(self):
        tplName = self.getBaseTemplate().getUid()
        return self.getPerfValue(tplName, "MwTomcat", "cThreadCount")

    def getCurrentPerfs(self):
        tplName = self.getBaseTemplate().getUid()
        
        cThreadCount = self.getPerfValue(tplName,"MwTomcat", "cThreadCount")
        cThreadsBusy = self.getPerfValue(tplName,"MwTomcat", "cThreadsBusy")
        
        totalMem = self.getPerfValue(tplName,"MwTomcat", "totalMem")
        freeMem = self.getPerfValue(tplName,"MwTomcat", "freeMem")
        
        mwVersion = self.getStatusValue(tplName,"MwTomcat", "mwVersion")
        osVersion = self.getStatusValue(tplName,"MwTomcat", "osVersion")
        jvmVersion = self.getStatusValue(tplName,"MwTomcat", "jvmVersion")
        
        reqPerSec = self.getPerfValue(tplName,"MwTomcat", "reqPerSec")
        bytesPerSec = self.getPerfValue(tplName,"MwTomcat", "bytesPerSec")
        errorPerSec = self.getPerfValue(tplName,"MwTomcat", "errorPerSec")
        
        return dict(
                        cThreadCount=cThreadCount,cThreadsBusy=cThreadsBusy,
                        totalMem=xutils.byte2readable(totalMem, False) ,freeMem=xutils.byte2readable(freeMem, False),
                        mwVersion=mwVersion,osVersion=osVersion,jvmVersion=jvmVersion,
                        reqPerSec=reqPerSec,bytesPerSec=bytesPerSec,errorPerSec=errorPerSec
                    )
    
    