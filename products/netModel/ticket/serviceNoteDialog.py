#coding=utf-8
'''
time:2014-12-22
@version: netbase4.0
@author: julian
'''
from products.netModel.baseModel import DocModel
from products.netModel import medata
import time

class ServiceNoteDialog(DocModel):
    '''
    time:2014-12-22
    @author: julian
    @todo: 工单对话对象的存储
    @param dbCollection: 存储对话对象的文档
    @param serviceNote: 对话发生的工单对象
    @param speaker: 对话人
    @param rTime: 对话时间，默认为当前时间
    @param content: 对话内容，默认为空
    '''
    dbCollection = 'ServiceNoteDialog'
    serviceNote = medata.doc("serviceNote")
    speaker = medata.doc("speaker")
    rTime = medata.plain("rTime", time.time())
    content = medata.plain("content", "")
    
    def __init__(self, uid=None):
        DocModel.__init__(self)
        self.__extMedata__(dict(
                
        ))
    
