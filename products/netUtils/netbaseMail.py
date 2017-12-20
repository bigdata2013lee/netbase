#coding=utf-8
###########################################################################
#       
#
#此软件版权为深圳商之杰科技有限公司所有,更多信息请访问www.netbase.asia
#
#
###########################################################################

__doc__ = """
邮件服务器
"""
import os
import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText 
from email.mime.image import MIMEImage
from products.netAlarm import settings
log = logging.getLogger("netalarm")
_mailObj={"mail":None,"isconnect":False}

def renewInitValue():   
    _mailObj["mail"]=None
    _mailObj["isconnect"]=False

class NetbaseMail(object):
    """
    netbase邮件发送类
    """
    def __init__(self,sername="smtp.exmail.qq.com",port="25",username="netbase@safedragon.com.cn",mailpwd=""):
        global  _mailObj  
        self.isSuccess=False     
        self.message =MIMEMultipart()
        self.smtp = smtplib.SMTP()
        self.smtp.connect(sername, port)
        self.smtp.login(username, mailpwd)
        self.username=username
        _mailObj["mail"]=self
        _mailObj["isconnect"]=True
        
    @property    
    def frommail(self,frommail):
        self.frommail=frommail
        
    @property    
    def tomail(self,tomail):
        """ 
         支持一个活多个发送地址，如有多个地址请以数组形式传入 
        """
        self.tomail=tomail
         
    @property
    def mailtitle(self,mailtitle):
        mailtitle=mailtitle.decode("utf-8")
        self.mailtitle=mailtitle
                    
    def addMultiAttachment(self,files=[]):
        """
                添加多个附件
                 注意：文件列表中的文件不支持作HTML中文件路径
        """
        for filepath in files:
            #获取附件名词
            filename=os.path.basename(filepath)
            if os.path.exists(filepath):
                tfile=filename.lower()
                pictureType=['jpg','jpeg','gif','png']  #图片后缀
                _cycFlag=True                
                for picture in pictureType:
                    if tfile.endswith(picture):
                        image = MIMEImage(open(filepath,'rb').read())
                        image.add_header("Content-ID", "attachment", filename = filename)
                        self.message.attach(image)
                        _cycFlag=False
                        break 
                if not _cycFlag:
                    continue
                text=MIMEText(open(filepath,"r").read(),"plain","utf-8")
                text.add_header('Content-Disposition',"attachment",filename=filename)
                self.message.attach(text)
        else:
            log.info("%s 文件不存在，请查证后再输入" %filepath)                                   
  
    def __setmail_information(self,mailfrom,mailto,mailtitle):
        """
                设置邮件基本信息
        @param mailfrom: 发件地址
        @param mailto:收件地址
        @param mailtitle: 邮件标题
        """      
        self.username= self.username+"<"+mailfrom+">"
        self.message["Subject"]=mailtitle
        self.message["From"]=self.username
        self.message['To']=mailto
    
    
    def addEmailContent(self,contentFun,files,displaytype="html"):
        """
                添加邮件内容
        @param alarmevent:事件对象
        @param displaytype:内容显示方式，默认按html形式显示
        plain：文本格式
         for example:
             <b>Some <i>HTML</i> text</b> and an image.<br><img src="cid:image1"><br>Nifty!'
        """
        self.addMultiAttachment(files)
        content=contentFun(self.message)
        msgText =MIMEText(content,displaytype,"utf-8")
        self.message.attach(msgText)
                         
    def send_mail(self):
        """
                邮件发送
        """ 
        frommail = self.frommail
        tomail = self.tomail
        mailtitle = self.mailtitle
        self.__setmail_information(frommail,tomail,mailtitle)
        msg = self.message
        try: 
            self.smtp.sendmail(frommail, tomail,msg.as_string())
            self.isSuccess=True
            return True
        except:
            log.error("连接失败，请检查发件人地址，或邮件配置")
        return self.isSuccess
              
    def disconnect_server(self):
        """
        断开服务器
        """
        if self.isSuccess:
            self.smtp.quit()
           
def getMailConfig(section,option):
        """
        获取邮件配置
        """
        return settings.getMailConfig(section, option)

def sendEmail(contentFun,mailtitle,tomail,files):
        """
                发送邮件
        """
        _mailConfig = settings._mailConfig
        #每套循环中，秩序第一次时加载邮件配置
        sername = getMailConfig("mailServer","sername")
        port = getMailConfig("mailServer","port")
        username = getMailConfig("sendUser","username")
        mailpwd = getMailConfig("sendUser","password")
        frommail=getMailConfig("sendUser","frommail")
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
    
        mail=NetbaseMail(sername, port, username, mailpwd)
        
        mail.frommail = frommail
        mail.mailtitle = mailtitle 
        mail.tomail = tomail
        mail.addEmailContent(contentFun,files)
        
        sendRs=mail.send_mail()
        mail.disconnect_server()
        return sendRs

