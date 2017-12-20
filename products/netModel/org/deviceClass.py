# coding=utf-8
from products.netModel.org.organizer import Organizer
from products.netModel.device import Device
from products.netPublicModel.userControl import UserControl
from products.netModel.eventSupport import DeviceClsOrgEventSupport

class DeviceClass(DeviceClsOrgEventSupport, Organizer):
    dbCollection = 'DeviceClass'
    rootUname = 'devicecls'




    def __init__(self, uname="", title=""):
        Organizer.__init__(self, uname=uname, title=title)

    def getCurMonitorObjs(self,conditions = {}):
        """
        getCurMonitorObjs
        """
        UserControl.addCtrlCondition(conditions)
        return self._getRefMeObjects('deviceCls', Device, conditions = conditions)
            




    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
