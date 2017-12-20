# coding=utf-8
from products.netModel.org.organizer import Organizer
from products.netModel.network import Network
from products.netPublicModel.userControl import UserControl
from products.netModel.eventSupport import OrgEventSupport

class NetworkClass(OrgEventSupport, Organizer):
    dbCollection = 'NetworkClass'
    rootUname = 'networkcls'


    def __init__(self, uname="", title=""):
        Organizer.__init__(self, uname=uname, title=title)

    def getCurMonitorObjs(self, conditions={}):
        """
        getCurMonitorObjs
        """
        UserControl.addCtrlCondition(conditions)
        return self._getRefMeObjects('networkCls', Network, conditions=conditions)
    


if __name__ == "__main__":
    x = NetworkClass.loadByGroupAndUname("firewall", "53743e10e138230b6221ed6e")
    print x


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
