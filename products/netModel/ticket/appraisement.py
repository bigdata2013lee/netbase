#coding=utf-8
'''
    time:2014-12-22
    @version: netbase4.0
    @author: julian
'''
from products.netModel.baseModel import DocModel
from products.netModel import medata
import time

class Appraisement(DocModel):
    '''
    time:2014-12-22
    @author: julian
    @todo: 对评价对象的存储和检索
    @param dbCollection: 存储评价对象的文档
    @param user: 评价人
    @param engineer: 被评价的工程师
    @param serviceNote: 被评价的工单
    @param attitude: 服务态度，由1-5五个数字组成，1,2表示差，3表示一般，4,5表示好，默认为3
    @param techLevel: 技术水平，由1-5五个数字组成，1,2表示差，3表示一般，4,5表示好，默认为3
    @param responseSpeed: 响应速度，由1-5五个数字组成，1,2表示差，3表示一般，4,5表示好，默认为3
    @param appraiseContent: 评价内容，默认为空
    @param appraiseTime: 评价时间，默认为服务器当前时间
    '''
    dbCollection = 'appraisement'
    user = medata.doc("user")
    engineer = medata.doc("engineer")
    serviceNote = medata.doc("serviceNote")
    attitude = medata.plain("attitude", 3)
    techLevel = medata.plain("techLevel", 3)
    responseSpeed = medata.plain("responseSpeed", 3)
    appraiseContent = medata.plain("appraiseContent", "")
    appraiseTime = medata.plain("appraiseTime", time.time())
    
    def __init__(self, uid=None):
        DocModel.__init__(self)
        self._medata.update(_id=uid)
    
    def getAppraisements(self, conditions={}):
        '''
        time:2014-12-22 
        @author: julian
        @todo: 检索评价对象
        @param conditions: 检索条件列表，默认为空
        @return: 检索出来的评价对象列表
        '''
        return self._getRefMeObjects("appraisement", Appraisement, conditions=conditions, sortInfo={"rTime":-1})
    
