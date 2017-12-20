#coding=utf-8
import md5
import re
import commands
from products.netUtils.xutils import nbPath as _p
isBuiltinColl = False  #内建收集器?内建收集器不需要运行授权

class CollectorLicense(object):
    
    
    @classmethod
    def createSn(cls, mac, company, collector):
        x1 = md5.new(mac).hexdigest().upper()
        x2 = md5.new(company).hexdigest().upper()
        x3 =  md5.new(collector).hexdigest().upper()
        x4 = md5.new("%s%s%s" %(x1,x2,x3)).hexdigest().upper()
        
        rx =  "M%sX%sS%sK%s" %(x1,x2,x3,x4)
        return rx
    
    @classmethod
    def  getMacList(cls):
        output = commands.getoutput("ifconfig -a | grep HWaddr")
        all = re.findall(r"[0-9a-zA-Z]{2}:[0-9a-zA-Z]{2}:[0-9a-zA-Z]{2}:[0-9a-zA-Z]{2}:[0-9a-zA-Z]{2}:[0-9a-zA-Z]{2}",repr(output))
        return all
    
    @classmethod
    def checkFormat(cls, sn):
        all = re.findall(r"M([0-9A-F]{32})X([0-9A-F]{32})S([0-9A-F]{32})K([0-9A-F]{32})", sn)
        
        if all:
            all = all[0]
            x123 = md5.new("".join(all[0:3])).hexdigest().upper()
            if x123 == all[3]: return all
            else:return []
        return []
    
    
    @classmethod
    def auth(cls, sn):
        macs = cls.getMacList()
        ks = cls.checkFormat(sn)
        if not ks:return False
        macK = ks[0]
        
        if macK not in [md5.new(mac.upper()).hexdigest().upper() for mac in macs]: return False
        
        return True
        
def _getSN():
        sn=""
        f=None
        try:
            f = open(_p("/.license.dat"))
            sn = "".join(f.readlines())
        except:
            pass
        
        finally:
            if f:f.close()
        return sn

def licenseAuth(func):
    """
    收集器license认证装饰方法
    @note: 内建收集器无需认证
    """
    def new_func(*args, **argkw):
        if not isBuiltinColl:
            sn = _getSN()
            if not CollectorLicense.auth(sn):return
            
        data = func(*args, **argkw)
        return data
    
    return new_func
        
@licenseAuth
def testStart():
    
    print "testStart"
    
if  __name__ == "__main__":
    sn="""M3FC2756D0AD747DD2B694E2BF75E96F7X739A5FF3EED4C1381D6B5D460EED34F5S104CB3FFB419EFEF7E188BAF0DE4426DK1780014273F5BA33495557E90B66C29C"""
    

    print CollectorLicense.createSn("mac", "company", "collector")
    
    
    