#coding:utf-8
'''
Created on 2013-8-26

@author: pwup
'''
import time
import logging
import ConfigParser
from products.netUtils.xutils import nbPath as _p

log = logging.getLogger("netalarm") 

_mail = dict(_isLoaded = False, cf = None)
_mailConfig={'sername':None,
             'port':25,
             'username':None,
             'mailpwd':None,
             'frommail':None,
             'isload':False
                               }
   
def _loadMailConf():
    """
    加载邮箱配置文件
    """
    cf=ConfigParser.ConfigParser()
    cf.read(_p("/etc/manager.conf")) 
    _mail["cf"] = cf
    _mail["_isLoaded"] = True
    
def getMailConfig(section, option):
    """
    获取配置文件字段
    '"""
    if not _mail["_isLoaded"]: _loadMailConf()
    _mailconf=None
    
    try:
        _mailconf=_mail['cf'].get(section, option).strip()
    except:
        log.exception("邮箱配置文件配置不正确，请检查")
        
        #当配置文件配置不正确时，需更新后才继续往下面执行，因此设置30s提示一次
        time.sleep(10)
        emptyMailObj()
        return getMailConfig(section, option)

    #当配置文件option值为空时报错 
    if _mailconf :
        return _mailconf
    else:        
        log.exception("邮箱配置文件配置不正确，请检查")
        #当配置文件配置不正确时，需更新后才继续往下面执行，因此设置30s提示一次
        time.sleep(10)
        emptyMailObj()
        return getMailConfig(section, option)
    
def emptyMailObj():
    """
     清空原加载配置对象
    """
    _mail["_isLoaded"] = False
    _mail["cf"] = None
    
def renewMailConfigInitValue():
    """
    清空配置文件字段
    """
    _mailConfig['sername']=None
    _mailConfig['port']=25
    _mailConfig['username']=None
    _mailConfig['mailpwd']=None
    _mailConfig['frommail']=None
    _mailConfig['isload']=False

if __name__=="__main__":
    print getMailConfig("server","sername")