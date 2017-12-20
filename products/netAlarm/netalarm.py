#coding=utf-8
import time
from bson import ObjectId  
from twisted.internet import reactor
from products.netUtils.manageBase import ManageBase
from products.netAlarm import settings
from products.netAlarm import alarmMail
from products.netAlarm import alarmRecord
from products.netUtils.xutils import getEventManager
from products.netPublicModel.baseConfigModel import ConfigServiceModel
from products.netModel.user.user import User
from products.netBilling.billingSys import BillingSys 
from products.netModel.weiXinAlarmRecord import WeiXinAlarmRecord
import logging
log = logging.getLogger("netalarm")
#告警模式


class AlarmAction(ConfigServiceModel):
    """
    告警事件类
    """ 
    
    def remoteAlarmMain(self):
        """
        告警主方法
        """
        self.processEvent()
    
    def processEvent(self):
        """
        处理事件
        """
        settings.emptyMailObj()#删除原配置文件对象
        settings.renewMailConfigInitValue()#删除原配置文件内容
        
        mailtitle = "netbase告警"
        
        #self.processRestoreEvent(mailtitle)
        userObjs=User._findObjects({})#获取用户对象
        for  userObj in userObjs:
            self.processUnRestoreEvent(userObj, mailtitle)
       
    def getMailConfig(self,section,option):
        """
        获取邮件配置
        """
        return settings.getMailConfig(section, option)
        
    def processUnRestoreEvent(self,userObj,mailtitle):
        """
        新增事件处理
        """
        ownCompany = userObj.ownCompany.getUid()
        if ownCompany is None:return
        usename=userObj.getUserName()
        alarmRules=userObj.getAlarmRules()
        for rule in alarmRules:
            condition = rule.conditions
            duration=condition["last"]
            del condition["last"]
            condition.update(dict(companyUid=ownCompany,historical=False))
            events = findEvents(condition)
            for event in events:
                alrc = alarmRecord.AlarmRecord()
                alarmEventId = event.getUid()
                if duration:
                    if event.endTime-event.firstTime<duration*60:continue
                #查询原记录表中当前用户是否存在这条事件，如存在则不加入记录表，防止同一家公司告警信息需要通知多人的情况
                if alrc.getAlarmRecordsNumByEventIdAndUser(alarmEventId,usename)>0:
                    continue
                message = event.message
                alarmUser = usename
                event.alarmUser = alarmUser
                sendRs=self.processSend(userObj,rule,mailtitle, event)
                #原记录表中不存在的事件需插入到记录表中                       
                if sendRs:alrc.addRecord(message, alarmEventId, alarmUser)             
                 
                                     
    def sendEmail(self,userObj,mailtitle,alarmevent,receivers):
        """
        发送邮件
        """
        _mailConfig = settings._mailConfig
        #每套循环中，秩序第一次时加载邮件配置
        if not _mailConfig['isload']:
            sername = self.getMailConfig("mailServer","sername")
            port = self.getMailConfig("mailServer","port")
            username = self.getMailConfig("sendUser","username")
            mailpwd = self.getMailConfig("sendUser","password")
            frommail=self.getMailConfig("sendUser","frommail")
            _mailConfig['sername'] = sername
            _mailConfig['port'] = port
            _mailConfig['username'] = username
            _mailConfig['mailpwd'] = mailpwd
            _mailConfig['frommail'] = frommail
            _mailConfig['isload'] = True
        sername = _mailConfig['sername']
        port = _mailConfig['port']
        username = _mailConfig['username']
        mailpwd = _mailConfig['mailpwd']
        frommail = _mailConfig['frommail']
        mail=alarmMail.AlarmCNMail(sername, port, username, mailpwd)
        
        mail.frommail = frommail
        mail.mailtitle = mailtitle
        mail.tomail =",".join(receivers)
        mail.addEmailContent(alarmevent)
        
        sendRs=mail.send_mail()
        mail.disconnect_server()
        return sendRs
                        
    def sendSMS(self,userObj,alarmtitle,alarmcontents,receivers):
        """
                发送短信
        """
        smsResult=True
        if not BillingSys.hasEnoughMoneyForSMS(userObj):
            print "%s用户余额不足,无法发送短信,请及时充值..."%userObj.username
            return False
        if smsResult:BillingSys.spendForSMS(userObj)
        return smsResult
    
    def sendMMS(self,userObj,alarmtitle,alarmcontents,receiver):
        """
                发送微信Micro Message Service
                
        """
        pass

    def processSend(self,userObj,rule,alarmtitle,alarmevent):        
        """
        处理通信方式
        """
        alarmMode = rule.alarmModel
        receivers=map(lambda x:str(x).strip(),rule.alarmReceive.split(","))
        if not receivers:return False
        funname="send%s"%alarmMode
        if not hasattr(self,funname):return False
        func=getattr(self,funname)
        sendRs=func(userObj,alarmtitle,alarmevent,receivers)
        return sendRs
        
class netalarm(ManageBase):
    """
    功能:alarm类
    作者:xwx
    时间:2013-8-30
    """
    alarmCycleInterval=120
    def __init__(self):
        ManageBase.__init__(self)
        
    def mainbody(self):
        """
        主循环
        """
        def afun(serviceObj=None):
            csm = serviceObj.getCSM(self.options.csmconfig)
            return csm.remoteAlarmMain()
        self.rpyc.access(afun)
    
    def runCycle(self):
        """
        循环运行
        """
        start = time.time()
        try:
            self.mainbody()
            log.info("运行告警规则消耗了%s", time.time()-start)
        except:
            log.exception("unexpected exception")
        reactor.callLater(self.alarmCycleInterval,self.runCycle)
    
    def run(self):
        """
        开始运行
        """
        import socket
        self.daemonHostname = socket.getfqdn()
        def startup():
            self.runCycle()
        reactor.callWhenRunning(startup)
        reactor.run()
        
    def buildOptions(self):
        ManageBase.buildOptions(self)
        self.parser.add_option('--csmconfig',dest = 'csmconfig',
                               default = 'AlarmAction',
                               help ='alarm守护进程配置类,默认为AlarmAction')
    
def findEvents(condition={}):
    """
    查询事件
    """
    mgr=getEventManager()
    _result=mgr.findEvents(conditions=condition)
    return _result
       
if __name__=="__main__":
    nam=netalarm()
    nam.run()
    
    
    