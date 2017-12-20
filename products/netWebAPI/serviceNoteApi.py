#coding=utf-8
'''
time:2014-12-22
@version: netbase4.0
@author: julian
'''
import os
import csv
import time
import codecs
from StringIO import StringIO
from products.netEvent.event import Event
from products.netUtils import jsonUtils, xutils
from products.netModel.user.user import User
from products.netUtils.xutils import nbPath as _p
from products.netModel.ticket.serviceNote import ServiceNote
from products.netPublicModel.userControl import UserControl
from products.netModel.user.engineerUser import EngineerUser
from products.netWebAPI.base import BaseApi
from products.netModel.ticket.appraisement import Appraisement
from products.netModel.ticket.serviceNoteDialog import ServiceNoteDialog
from products.netPublicModel.emailTemplates import new_service_note_mail_html

class ServiceNoteApi(BaseApi):
    '''
    time:2014-12-22
    @author: julian
    @todo: 工单的API接口类
    '''
    def createServiceNote(self, serviceNote):
        '''
        time:2014-12-22
        @author: juilan
        @todo: 创建工单
        @param serviceNote: 要创建工单对象
        @return: 创建成功与否的提示信息
        '''
        #判定用户是否有服务工程师
        customer = UserControl.getUser()
        eng = customer.engineer
        if not eng:
            return "warn:暂没有技术工程师为您服务,创建服务单失败，请联系客服工作人员"
        
        #判定生成工单的事件对象是否合法
        eventId = serviceNote.get("eventId","")
        if not eventId: return "warn:无法获得事件的ID信息"
        event = Event._loadObj(eventId)
        if not event:return "warn:该工单已经不存在"
        
        #判定工单的主题是否合法
        subject=serviceNote.get("subject","")
        if not subject:return "warn:请输入工单主题"
        if len(subject)>40:return "warn:主题最多40个字符，一个汉字算2个字符"
        
        #判定工单时间期限是否合法
        dueTime=serviceNote.get("dueTime","")
        if not dueTime:return "warn:请选择时间期限"
        nt=xutils.dealTime(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),"-",":")
        nt=int(nt[0:8])
        dt=dueTime.split(".")[0].replace("T"," ")
        dt=int(xutils.dealTime(dt,"-",":")[0:8])
        if nt>dt:return "warn:时间期限必须比当前时间晚"
        
        #判定工单的内容是否合法
        content=serviceNote.get("content","")
        if len(content)>2000:return "warn:内容最多2000个字符，一个汉字算2个字符"
        if not content:return "warn:请输入工单内容"

        #获取工单的状态和紧急度        
        status=serviceNote.get("status",0)
        emergencyDegree=serviceNote.get("emergencyDegree","紧急")
        
        #创建工单对象
        sn = ServiceNote()
        sn.event = event
        sn.user = customer
        sn.engineer = eng
        sn.status = status
        sn.subject = subject
        sn.dueTime = dueTime
        sn.emergencyDegree = emergencyDegree
        sn.content = content
        sn.startTime = int(time.time())
        sn._saveObj()

        #发送通知邮件给服务工程师
        try:    
            self.newServiceNoteMail(sn)
        except:
            return "创建服务单成功,但暂时无法发送邮件"
        return "创建服务单成功!"
    
    def delServiceNote(self,snId):
        '''
        time:2014-12-22
        @author: julian
        @todo: 删除工单
        @param snId:要删除的工单ID
        @return: 删除工单成功与否的提示信息 
        '''
        #检查工单与用户是否存在
        sn = ServiceNote._loadObj(snId)
        if not sn:return "warn:此工单不存在"
        user=UserControl.getUser()
        if not user:return "warn:请先登录"
        
        #检查该工单下是否有对话，有则删除
        dialogs=ServiceNoteDialog._findObjects({"serviceNote":sn._getRefInfo()})
        if dialogs:
            for dialog in dialogs:
                dialog.remove()
        
        #检查该工单下是否有附件，有则删除
        attachments = sn.attachments
        if attachments:
            for attach in attachments:
                subPath="/nbfiles/upload/%s" %attach
                path=_p(subPath)
                if os.path.exists(path):os.remove(path)
                
        #删除工单
        sn.remove()
        return "删除成功"
    
    def newServiceNoteMail(self,sn):
        '''
        time:2014-12-22
        @author: julian
        @todo: 创建工单时发送邮件给用户的服务工程师
        @param sn:被创建的工单对象
        '''       
        subject ="服务单通知"
        message = new_service_note_mail_html %{
                                                   "eventlabel":sn.event.label,
                                                   "monitorObjName":sn.monitorObjName,
                                                   "content":sn.content,
                                                   "startTime":sn.startTime,
                                                   "dueTime":sn.dueTime,
                                                   "emergencyDegree":sn.emergencyDegree,
                                                   "user":sn.user.username,
                                                   "eventMessage":sn.event.message
                                                }
        xutils.sendMail(subject, message, recipient_list=[sn.engineer.username], attachments=[]) 
     
    def getServiceNotes(self,  conditions={},  sortInfo=None, skip=0, limit=100):
        '''
        time:2014-12-22
        @author: julian
        @todo: 获取工单列表
        @param conditions: 获取工单的条件，默认为空
        @param sortInfo: 对获取结果的排序信息，默认为空
        @param skip:跳过的记录数，默认为0
        @param limit:限制的记录数，默认为100
        @return: 查询到的工单的列表  
        '''

        #设置查询条件
        user = UserControl.getUser()
        name = user.__class__.__name__
        usersRefinfos=[]
        if not user:return []
        if name =="User":
            conditions.update({"user":user._getRefInfo()})
        elif name=="EngineerUser":
            eng = user
            conditions.update({"engineer":eng._getRefInfo()})
        elif name=="Operationer":
            op = user
            users = User._findObjects({"operationer":op._getRefInfo()})
            for  u in users:
                usersRefinfos.append(u._getRefInfo()) 
            conditions.update({"user":{"$in":usersRefinfos}})

        #获取查询结果
        notes = ServiceNote._findObjects(conditions=conditions, sortInfo=sortInfo, skip=skip, limit=limit)
        objectCount = ServiceNote._countObjects(conditions=conditions)
        return {"total":objectCount, "results": notes}
    
    def checkoutServiceNotesAsCVS(self,conditions={},  sortInfo=None): 
        '''
        time:2014-12-22
        @author: julian
        @todo: 导出工单为附件
        @param conditions: 检索工单的条件，默认为空
        @param sortInfo: 对检索结果的排序信息，默认为None
        @return: 工单的附件文件
        '''
        #获取要导出的工单列表      
        rs = self.getServiceNotes(conditions=conditions, sortInfo=sortInfo, skip=0, limit=None)
        
        #创建文件，建立IO通道
        csvfile = StringIO()
        writer = csv.writer(csvfile)
        titles = ["主题", "名称/设备IP", "监控项目", "工单信息" ,"工程师" ,"开始时间", "结束时间", "紧急程度"]
        writer.writerow(titles)
        
        #定义写入格式，开始写入文件
        for r in rs.get("results",[]):
            label=""
            componentType=""
            titleOrUid=""
            if r.event:
                label=r.event.label
                componentType=r.event.componentType
            if r.user:
                titleOrUid=r.user.engineer.titleOrUid()
            listr = [r.subject, label, componentType, r.content, titleOrUid,
                     xutils.formartTime(r.startTime, fm="%Y-%m-%d %H:%M") ,
                     xutils.formartTime(r.endTime, fm="%Y-%m-%d %H:%M") ,
                      r.emergencyDegree]
            writer.writerow(listr)
        
        #定义文件编码
        csvfile = codecs.EncodedFile(csvfile, "gbk", "utf-8")
        return csvfile
        
    def checkoutAppraisementsAsCVS(self,sortInfo,conditions={}):
        '''
        time:2014-12-22
        @author: julian
        @todo: 导出评价为附件
        @param sortInfo: 对检索结果的排序信息
        @param conditions: 检索条件信息，默认为空
        @return: 评价的附件文件
        '''
        #获取评价列表       
        rs = self.getAppraisements(sortInfo,conditions=conditions)
        
        #创建文件，建立IO通道    
        csvfile = StringIO()
        writer = csv.writer(csvfile)        
        titles = ["工程师", "好评", "中评", "差评" ,"好评率" ]
        writer.writerow(titles)
        
        #定义评价的格式，写入文件        
        for r in rs:
            listr = [r.originalName, r.appraisement["good"], r.appraisement["common"], r.appraisement["bad"], r.appraisement["goodRate"]]
            writer.writerow(listr)
        
        #设置文件编码        
        csvfile = codecs.EncodedFile(csvfile, "gbk", "utf-8")
        return csvfile


    def checkoutEngAppraisementsAsCVS(self,engId,sortInfo,conditions={}):
        '''
        time:2014-12-22
        @author: julian
        @todo: 将工程师的评价详细导出为附件
        @param engId: 评价被导出的工程师ID
        @param sortInfo: 导出内容的排序信息
        @param conditions: 导出内容的检索条件，默认为空
        @return: 工程师评价的附件文件
        '''
        #获取工程师的评价内容
        rs = self.getEngineerAppr(engId,sortInfo,conditions=conditions)
        
        #创建附件文件，建立IO通道  
        csvfile = StringIO()
        writer = csv.writer(csvfile)        
        titles = ["评价时间", "工单主题", "客户", "工程师" ,"服务态度","专业水平","响应速度","评价内容" ]
        writer.writerow(titles)
        
        #定义工程师评价的格式，写入文件        
        for r in rs:
            subject=""
            username=""
            originalName=""
            if r.serviceNote:subject=r.serviceNote.subject
            if r.user:username=r.user.username
            if r.engineer:originalName=r.engineer.originalName
            listr = [xutils.formartTime(r.appraiseTime, fm="%Y-%m-%d %H:%M"), subject, username, originalName, r.attitude, r.techLevel, r.responseSpeed, r.appraiseContent]
            writer.writerow(listr)
            
        #定义附件的文件编码格式        
        csvfile = codecs.EncodedFile(csvfile, "gbk", "utf-8")
        return csvfile
    
    
    def getDialogs(self, snUid, conditions={},toJson=True):
        '''
        time:2014-12-22
        @author: julian
        @todo: 获取工单的对话
        @param snUid: 工单的ID
        @param conditions: 获取对话的条件，默认为空
        @param toJson: 是否转换为JSON对象，默认为True
        @return: 对话列表  
        '''
        sn = ServiceNote._loadObj(snUid)
        if not sn: return "warn:该工单不存在"
        rs = sn.getDialogs(conditions=conditions)
        def updict(obj):
            return dict(
                        speaker = obj.speaker and obj.speaker.titleOrUid(),
                        speakerType = obj.speaker and obj.speaker.__class__.__name__
            )
        rs.reverse()
        if not toJson:return rs
        return jsonUtils.jsonDocList(rs, updict=updict)
    
    def addDialog(self, snUid, content):
        '''
        time:2014-12-22
        @author: julian
        @todo: 添加工单对话
        @param snUid: 工单的UID
        @param content: 对话的内容
        @return: 添加对话的提示信息
        '''
        #发表对话的必要条件检测
        user = UserControl.getUser()
        if not user:return "warn:请先登录"
        if user.__class__.__name__ =="User":
            if not user.engineer:return "warn:您已经没有服务工程师，不可发表对话"
        if user.__class__.__name__ == "Engineer":
            if not User._findObjects({"engineer":user._getRefInfo()}):return "您没有服务的客户，不可发表会话"
        
        sn = ServiceNote._loadObj(snUid)
        if not sn: return "warn:该工单已经不存在！"
        if not content:return "warn:内容为必填项"
        if len(content)>2000:return "warn:内容最多2000个字符，一个汉字算2个字符"
        if xutils.addAttachment(self.request,sn) !="success":return "附件发送失败"
        
        #创建工单对话
        snDialog = ServiceNoteDialog()
        snDialog.content = content
        snDialog.speaker = user
        snDialog.rTime=time.time()
        snDialog.serviceNote=sn
        snDialog._saveObj()
        return "success"
    
    def getAttachments(self, snUid):
        '''
        time:2014-12-22
        @author: julian
        @todo: 获得附件列表
        @param snUid: 工单的ID号
        @return: 工单的附件列表
        '''
        sn = ServiceNote._loadObj(snUid)
        if not sn: return []
        return sn.attachments
    
    def appraise(self,attitude=5,techLevel=5,responseSpeed=5,appraiseContent="",ticketId=""):
        '''
        time:2014-12-22
        @author: julian
        @todo: 评价工程师
        @param user:评价人
        @param engineer:被评价的人
        @param ticketId: 被评价的工单号
        @param attitude: 态度，1为很差，2为较差，3为一般，4为较好，5为非常好
        @param techLevel: 技术水平，1为很差，2为较差，3为一般，4为较好，5为非常好
        @param responseSpeed: 对工单的响应速度，1为很差，2为较差，3为一般，4为较好，5为非常好
        @param appraiseContent: 评价的内容
        @return 评价的提示消息 
        '''
        #评价前的必要性条件检查
        user = UserControl.getUser()
        if not user:return "warn:请先登录"
        serviceNote=ServiceNote._loadObj(ticketId)
        if not serviceNote:return "warn:该服务单已不存在"
        engineer = serviceNote.engineer
        if not engineer:return "warn:该工程师不存在"
        if len(appraiseContent)>2000:return "warn:内容最多2000个字符，一个汉字算2个字符"
        
        #生成评价对象
        appraisement = Appraisement()
        appraisement.user=user
        appraisement.engineer=engineer
        appraisement.serviceNote=serviceNote
        attitude=int(attitude)
        techLevel=int(techLevel)
        responseSpeed=int(responseSpeed)
        
        #计算综合得分，给出评价等级
        if attitude < 1 or attitude > 5:attitude=3
        if techLevel < 1 or techLevel > 5:techLevel=3
        if responseSpeed < 1 or responseSpeed > 5:responseSpeed=3
        total=attitude+techLevel+responseSpeed
        appr="common"
        if total > 0 and total < 7:appr="bad"
        if total >6 and total < 11:appr="common"
        if total >10 and total < 16:appr="good"
        appraisement.attitude=attitude
        appraisement.techLevel=techLevel
        appraisement.responseSpeed=responseSpeed
        appraisement.appraiseContent=appraiseContent
        appraisement._saveObj()
        
        #相同用户首次评价时，更新好评率，否则不更新
        conditions={"user":user._getRefInfo()}
        conditions.update({"engineer":engineer._getRefInfo()})
        conditions.update({"serviceNote":serviceNote._getRefInfo()})
        appts=Appraisement._findObjects(conditions)
        if len(appts)<2:
            appt=engineer.appraisement
            if not appt:appt={"good":0,"common":0,"bad":0,"goodRate":0.00}
            appt[appr]=appt[appr]+1
            appt["goodRate"]=round(appt["good"]*1.0/(appt["good"]+appt["common"]+appt["bad"]),2)
            engineer.appraisement=appt
            engineer._saveProperty()
        return "感谢您的评价"
        
    def changeTicketStatus(self,serviceNote):
        '''
        time:2014-12-22
        @author: julian
        @todo: 改变工单状态
        @param serviceNote: 工单对象
        '''
        #表要条件检查
        user=UserControl.getUser()
        if not user:return "warn:请先登录"
        if user.__class__.__name__ == "User":
            if not user.engineer:return "warn:暂时没有工程师为您服务，不可打开工单"
        sid=serviceNote.get("sid","")
        if not sid:return "warn:没有得到工单的id信息"
        sn = ServiceNote._loadObj(sid)
        if not sn:return "warn:该工单已经不存在"
        
        #检测status的状态值，符合条件则改变
        status=int(serviceNote.get("status","-1"))
        if status == -1:return "不需要改变工单的状态"
        if status not in [0,1]:return "warn:不正确的工单状态值"
        if sn.status != status:sn.status=status
        
        #如果由打开改成关闭，需要更新结束时间，反之，需要更新开始时间
        if status==0:
            sn.startTime=int(time.time())
            if user.__class__.__name__ == "User":sn.engineer=user.engineer
        if status==1:sn.endTime=int(time.time())
    
    def getAppraisements(self,sortInfo, conditions={}):
        '''
        time:2014-12-22
        @author: julian
        @todo: 获取所有工程师的好评率
        @return: 返回工程师的评价列表
        '''
        appraisements = EngineerUser._findObjects(conditions=conditions, sortInfo=sortInfo)
        return appraisements
    
    def getEngineerAppr(self,engId,sortInfo,conditions={}):
        '''
        time:2014-12-22
        @author: julian
        @todo: 获取某个工程师的评价
        @param engId: 工程师ID
        @param sortInfo: 获取评价的排序信息
        @param conditions: 获取评价的检索条件
        @return: 工程师的评价对象列表
        '''
        eng=EngineerUser._loadObj(engId)
        conditions={"engineer":eng._getRefInfo()}
        appraisements=Appraisement._findObjects(conditions=conditions, sortInfo=sortInfo)
        return appraisements
    