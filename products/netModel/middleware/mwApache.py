#coding=utf-8
from products.netModel import medata
from products.netModel.middleware.mwBase import MwBase
from products.netUtils.xutils import nbPath as _p
from products.netUtils import xutils
class MwApache(MwBase):
    dbCollection = 'MwApache'
    def __init__(self, uid=None):
        MwBase.__init__(self)
        
    host = medata.plain("host","")
    port = medata.plain("port",80)
    url = medata.plain("url", "/server-status?auto")
    ssl =medata.plain("ssl",False)
    ngregex = medata.plain("ngregex", "")
    ngerror = medata.plain("ngerror", "")
    httpUsername = medata.plain("httpUsername","")
    httpPassword = medata.plain("httpPassword","")
    
    def getManageId(self):
        """
                获取apache对象的管理Id
        """
        return self.host
    
    def getCmd(self):
        """
                获取命令
        """
        parts = [_p("/bin/python") ,_p("/products/netCommand/pyexec/check_apache.py")]
        if self.host:
            parts.append('-H %s' % self.host)
        if self.port:
            parts.append('-p %s' % self.port)
        if self.ssl:
            parts.append('-s %s' % self.ssl)
        if self.url:
            parts.append("-u '%s'" % self.url)
        if self.ngregex:
            parts.append("-r '%s'" % self.ngregex)
            if self.ngerror:
                parts.append("-e '%s'" % self.ngerror)
        if self.httpUsername:
            parts.append('--username %s' % self.httpUsername)
        if self.httpPassword:
            parts.append('--password %s' % self.httpPassword)
        cmd = ' '.join(parts)
        return cmd
    
    
    def getConnCount(self):
        tplName = self.getBaseTemplate().getUid()
        return self.getPerfValue(tplName, "MwApache", "connection")
    
    def getCurrentPerfs(self):
        tplName = self.getBaseTemplate().getUid()
        mwVersion = self.getStatusValue(tplName,"MwApache", "mwVersion")
        connection = self.getPerfValue(tplName,"MwApache", "connection")
        reqPerSec = self.getPerfValue(tplName,"MwApache", "reqPerSec")
        bytesPerSec = self.getPerfValue(tplName,"MwApache", "bytesPerSec")
        upTime = self.getStatusValue(tplName,"MwApache", "upTime")
        return dict(connection=connection, reqPerSec=reqPerSec, bytesPerSec=bytesPerSec, upTime=xutils.sec2UseTime(upTime),mwVersion=mwVersion)
    
    