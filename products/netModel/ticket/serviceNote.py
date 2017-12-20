#coding=utf-8
'''
time:2014-12-22
@version: netbase4.0
@author: julian
'''
from products.netModel.baseModel import DocModel
from products.netModel import medata
from products.netModel.ticket.serviceNoteDialog import ServiceNoteDialog
import time

class ServiceNote(DocModel):
    '''
    time:2014-12-22
    @author: juilan
    @todo: 对工单对象的存储和检索工单的对话
    @param dbCollection: 存储工单对象的文档
    @param user: 工单的创建人
    @param engineer: 工单的负责工程师
    @param event: 触发生成工单的事件
    @param subject: 工单的主题
    @param dueTime: 工单的处理期限，默认为当前事件
    @param emergencyDegree: 工单的紧急度，默认为紧急
    @param content: 工单的内容描述，默认为空
    @param startTime: 工单的开始时间，默认为当前时间
    @param endTime: 工单的结束时间，默认为当前时间
    @param status: 工单的状态，0-打开，1-关闭
    @param attachments: 工单的附件列表，默认为空
    '''
    dbCollection = 'ServiceNote'
    user = medata.doc("user")
    engineer = medata.doc("engineer")
    event = medata.doc("event")
    subject = medata.plain("subject", "")
    dueTime = medata.plain("dueTime", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    emergencyDegree = medata.plain("emergencyDegree", "紧急")
    content = medata.plain("content", "")
    startTime = medata.plain("startTime", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    endTime = medata.plain("endTime", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    status = medata.plain("status", 0)
    attachments = medata.plain("attachments", [])
    
    def __init__(self, uid=None):
        DocModel.__init__(self)
        self._medata.update(_id=uid)

    def getDialogs(self, conditions={}):
        '''
        time:2014-12-22
        @author: julian
        @todo:根据工单对象检索其对话列表
        @param conditions:检索条件列表，默认为空
        @return: 检索出来的对话结果列表
        '''
        return self._getRefMeObjects("serviceNote", ServiceNoteDialog, conditions=conditions, sortInfo={"rTime":-1})
