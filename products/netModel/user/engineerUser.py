#coding=utf-8
from products.netModel.user.user import User
from products.netModel.user.baseUser import BaseUser
from products.netModel import medata
from products.netModel.ticket.serviceNote import ServiceNote

class EngineerUser(BaseUser):
    dbCollection = 'EngineerUser'
    
    def __init__(self,uid=None):
        BaseUser.__init__(self, uid)


    operationer = medata.doc("operationer")  #运维商
    appraisement = medata.plain("appraisement",{"good":0,"common":0,"bad":0,"goodRate":0.00})  #评价
    @property
    def users(self):
        """
        用户列表
        """ 
        return self._getRefMeObjects("engineer",User, conditions={})
        

    def getServiceNotes(self, conditions={}):
        return self._getRefMeObjects("engineer", ServiceNote, conditions=conditions)
    
    def getScore(self):
        """
        得到平均分数
        """
        conditions = {"status": 2, "engineer": self._getRefInfo()}
        notes = self.getServiceNotes(conditions=conditions)
        totalScore = 0
        for note in notes: totalScore += note.score
        if not notes:return 0
        return totalScore / len(notes)


    
