#coding=utf-8
from products.netModel.user.user import User
from products.netModel.org.location import Location
from products.netModel.device import Device
from products.netModel.network import Network

def createLocRoot():
    users = User._findObjects()
    for u in users:
        company = u.ownCompany
        locs = company._getRefMeObjects("ownCompany", Location, conditions={"uname":"location"})
        loc = None
        if locs: loc = locs[0]
        if not locs:
            loc = Location(uname=Location.rootUname,title="分组")
            loc.ownCompany = company
            loc._saveObj()
            print "Creatting loc root for user[%s]" %u.username
            
        
        hostDevs = company._getRefMeObjects("ownCompany", Device)
        for dev in hostDevs:
            if not dev.location:
                dev.location = loc
                
        
        networkDevs = company._getRefMeObjects("ownCompany", Network)
        for dev in networkDevs:
            if not dev.location:
                dev.location = loc
    