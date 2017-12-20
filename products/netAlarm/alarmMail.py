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
邮件处理器
"""
import os
import time
import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText 
from email.mime.image import MIMEImage
log = logging.getLogger("netalarm")

_mailObj={"mail":None,"isconnect":False}

emailTplPath=_p("/products/netAlarm/emailTemplate/")

monitorMap={"Website":"站点","Device":"主机","Network":"网络","Bootpo":"开机","Process":"进程","IpInterface":"接口",
        "IpService":"Ip服务","FileSystem":"磁盘"}

def renewInitValue():   
    _mailObj["mail"]=None
    _mailObj["isconnect"]=False

class AlarmCNMail():
    def __init__(self,sername="smtp.exmail.qq.com",port="25",username="netbase@safedragon.com.cn",mailpwd=""):
        global  _mailObj  
        self.isSuccess=False     
        self.message =MIMEMultipart()
        self.smtp = smtplib.SMTP()
        #self.smtp.set_debuglevel(1)
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
        '''
         添加多个附件
         注意：文件列表中的文件不支持作HTML中文件路径，如需要设置html路径请单独调用 
         addOnePictureAttachment方法
        '''
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

    def addOnePictureAttachment(self,filepath,tagid=""):
        """
        添加一个图片附件
        @param filepath: 附件路径
        @param id:html标签ID   
        """
        filename=os.path.basename(filepath)
        if os.path.exists(filepath):   
            tfile=filename.lower()
            pictureType=['jpg','jpeg','gif','png']  
            _value="attachment"                      
            for picture in pictureType:
                if tfile.endswith(picture):
                    image = MIMEImage(open(filepath,'rb').read())
                    #当格式是HTML时，如果需要显示图片则需要把图片作为附件发送
                    tagid=str(tagid).strip()
                    if tagid is not None or tagid !="":
                        tagid="<"+tagid+">"
                        _value=tagid  
                        image.add_header("Content-ID", _value)
                    else:
                        image.add_header("Content-ID", _value, filename = filename)
                    self.message.attach(image)
        else:
            log.info("The %s file path does not exist!" %filename)          
            
                             
    def addOneTextAttachment(self,filepath):
        """
        添加文本附件 
        @param filepath: 附件路径
        """
        filename=os.path.basename(filepath)
        if os.path.exists(filepath):
            text=MIMEText(open(filepath,"r").read(),"plain","utf-8")
            text.add_header('Content-Disposition',"attachment",filename=filename)
            self.message.attach(text)
            return                 
        else:
            log.info("The %s file path does not exist!" %filepath)
                                    
  
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
        
    def getHtmlContent(self):
        """
                得到邮件的html内容
        """
        emailTextPath="%s%s" %(emailTplPath,"index.html")
        html = open(emailTextPath).read() #读取HTML模板
        return html
    
    def getLogoImg(self):
        """
                得到Logo图片
        """
        emailImgPath="%s%s" %(emailTplPath,"images/logo.png")
        fp = open(emailImgPath, 'rb')  
        msgImage = MIMEImage(fp.read())  
        fp.close()  
        msgImage.add_header('Content-ID', '<logo>')  
        return msgImage
    
    def getQQImg(self):
        """
                得到QQ图片
        """
        emailImgPath="%s%s" %(emailTplPath,"images/qq.png")
        fp = open(emailImgPath, 'rb')  
        msgImage = MIMEImage(fp.read())  
        fp.close()  
        msgImage.add_header('Content-ID', '<qq>')  
        return msgImage
    
    def getWeiXinImg(self):
        """
                得到微信图片
        """
        emailImgPath="%s%s" %(emailTplPath,"images/weixin_be.jpg")
        fp = open(emailImgPath, 'rb')  
        msgImage = MIMEImage(fp.read())  
        fp.close()  
        msgImage.add_header('Content-ID', '<wenxin>')  
        return msgImage
    
    def getPhoneImg(self):
        """
                得到电话图片
        """
        emailImgPath="%s%s" %(emailTplPath,"images/phone_tp.jpg")
        fp = open(emailImgPath, 'rb')  
        msgImage = MIMEImage(fp.read())  
        fp.close()  
        msgImage.add_header('Content-ID', '<phone>')  
        return msgImage
    
    def getAdveImg(self):
        """
                得到广告图片
        """
        emailImgPath="%s%s" %(emailTplPath,"images/Adve01.jpg")
        fp = open(emailImgPath, 'rb')  
        msgImage = MIMEImage(fp.read())  
        fp.close()  
        msgImage.add_header('Content-ID', '<adve>')  
        return msgImage
    
    def getT01Img(self):
        emailImgPath="%s%s" %(emailTplPath,"images/t01.jpg")
        fp = open(emailImgPath, 'rb')  
        msgImage = MIMEImage(fp.read())  
        fp.close()  
        msgImage.add_header('Content-ID', '<t01>')  
        return msgImage
    
    def getT02Img(self):
        emailImgPath="%s%s" %(emailTplPath,"images/t02.png")
        fp = open(emailImgPath, 'rb')  
        msgImage = MIMEImage(fp.read())  
        fp.close()  
        msgImage.add_header('Content-ID', '<t02>')  
        return msgImage
    
    def getT03Img(self):
        emailImgPath="%s%s" %(emailTplPath,"images/t03.jpg")
        fp = open(emailImgPath, 'rb')  
        msgImage = MIMEImage(fp.read())  
        fp.close()  
        msgImage.add_header('Content-ID','<t03>')  
        return msgImage
        
    def addEmailContent(self,alarmevent,displaytype="html"):
        """
                添加邮件内容
        @param alarmevent:事件对象
        @param displaytype:内容显示方式，默认按html形式显示
        plain：文本格式
         for example:
             <b>Some <i>HTML</i> text</b> and an image.<br><img src="cid:image1"><br>Nifty!'
        """
        label=alarmevent._medata.get("label","")
        if not label:label=alarmevent.title,
        data=dict(label=label,
                  alarmUser=alarmevent.alarmUser,
                  message=alarmevent.message,
                  componentType=monitorMap[alarmevent.componentType],
                  firstTime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(alarmevent.firstTime))),
                  endTime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(alarmevent.endTime))),
                  count=alarmevent.count)
        evnet_alert_html=self.getHtmlContent()
        content=evnet_alert_html%data
        msgText =MIMEText(content,displaytype,"utf-8")
        self.message.attach(msgText)
        self.message.attach(self.getLogoImg())
        self.message.attach(self.getQQImg())
        self.message.attach(self.getWeiXinImg())
        self.message.attach(self.getPhoneImg())
        self.message.attach(self.getAdveImg())
        self.message.attach(self.getT01Img())
        self.message.attach(self.getT02Img())
        self.message.attach(self.getT03Img())
                         
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
           


