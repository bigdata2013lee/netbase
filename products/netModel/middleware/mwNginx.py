#coding=utf-8
from products.netModel.middleware.mwBase import MwBase
from products.netModel import medata
from products.netUtils.xutils import nbPath as _p

class MwNginx(MwBase):
    dbCollection = 'MwNginx'
    def __init__(self, uid=None):
        MwBase.__init__(self)
        
    host = medata.plain("host") #IP
    port = medata.plain("port", 80)
    ssl = medata.plain("ssl", False)
    url = medata.plain("url", "/nginx-status")  
    httpUsername = medata.plain("httpUsername", "")
    httpPassword = medata.plain("httpPassword", "") 
    
    def getManageId(self):
        """
                获取nginx对象的管理Id
        """
        return self.host
    
    def getCmd(self):
        """
        得到中间件的命令
        """
        parts = [_p("/bin/python") ,_p("/products/netCommand/pyexec/check_nginx.py")]
        
        if self.host:
            parts.append('-H %s' % self.host)
        if self.port:
            parts.append('-p %s' % self.port)
        if self.ssl:
            parts.append('-s %s' % self.ssl)
        if self.url:
            parts.append('-u %s' % self.url)
        if self.httpUsername:
            parts.append('--username %s' % self.httpUsername)
        if self.httpPassword:
            parts.append('--password %s' % self.httpPassword)
            
        cmd = ' '.join(parts)
        return cmd
    
    
        
        
    def getConnCount(self):
        tplName = self.getBaseTemplate().getUid()
        return self.getPerfValue(tplName,"MwNginx", "connection")
    
    def getCurrentPerfs(self):
        tplName = self.getBaseTemplate().getUid()
        connection = self.getPerfValue(tplName,"MwNginx", "connection")
        reqPerSec = self.getPerfValue(tplName,"MwNginx", "reqPerSec")
        errorPerSec = self.getPerfValue(tplName,"MwNginx", "errorPerSec")
        mwVersion = self.getStatusValue(tplName,"MwNginx", "mwVersion")
        return dict(connection=connection, reqPerSec=reqPerSec, errorPerSec=errorPerSec, mwVersion=mwVersion)
        
