# coding=utf-8
from products.netModel.org.organizer import Organizer
from products.netModel.website import Website
from products.netPublicModel.userControl import UserControl
from products.netModel.eventSupport import OrgEventSupport

class WebSiteClass(OrgEventSupport, Organizer):
    dbCollection = 'WebSiteClass'
    rootUname = 'websitecls'




    def __init__(self, uname="", title=""):
        Organizer.__init__(self, uname=uname, title=title)
        self._plugins = []
        
        self._template = None

    def getCurMonitorObjs(self, conditions={}):
        """
        getCurMonitorObjs
        """
        UserControl.addCtrlCondition(conditions)
        return self._getRefMeObjects('webSiteClass', Website, conditions=conditions)



    
    
    
    @classmethod
    def getRoot(cls):
        _condition={"uname":cls.rootUname}
        UserControl.addCtrlCondition(_condition)
        
        tb = cls._getDbTable()
        mObj = tb.find_one(_condition)
        if not mObj:return None
        root = cls._loadObjFromMap(mObj)
        return root
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
