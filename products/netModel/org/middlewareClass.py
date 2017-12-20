# coding=utf-8
from products.netModel.org.organizer import Organizer
from products.netPublicModel.userControl import UserControl
from products.netModel.eventSupport import OrgEventSupport
from products.netModel.middleware.mwBase import MwBase


class MiddlewareClass(OrgEventSupport,Organizer):
    dbCollection = 'MiddlewareClass'
    rootUname = 'middlewarecls'


    def __init__(self, uname="", title=""):
        Organizer.__init__(self, uname=uname, title=title)


    def getCurMonitorObjs(self, conditions={}):
        """
        getCurMonitorObjs
        """
        UserControl.addCtrlCondition(conditions)
        
        cls = MwBase.getSubMwCls(self.uname)
        if not cls : return []
        objs = self._getRefMeObjects('middlewareClass', cls, conditions=conditions)
        return objs
        

        