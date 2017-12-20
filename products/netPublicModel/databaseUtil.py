#coding=utf-8
import json
import os
import sys
from products.netModel.user.user import User
from products.netModel.company import Company
from products.netModel.device import Device
from products.netModel.website import Website
from products.netModel.network import Network
from products.netModel.shortcutCmd import ShortcutCmd
from products.netModel.bootpo import Bootpo
from products.netModel.collector import Collector
from products.netModel.devComponents.ipInterface import IpInterface
from products.netModel.devComponents.process import Process
from products.netModel.devComponents.filesystem import FileSystem
from products.netModel.devComponents.IpService import IpService
from products.netModel.org.location import Location
from products.netModel.org.webSiteClass import WebSiteClass
from products.netReport.reportRule import ReportRule
from products.netUtils import jsonUtils
from products.netUtils import xutils


class DataBaseUtil(object):
    def __init__(self): 
        self.clsTypes = [IpService, FileSystem, Process, Collector, IpInterface, User,Company, Device, Website,
         Network, ShortcutCmd, Bootpo,Location,WebSiteClass,ReportRule]
        self.filePath = "/opt/netbase4/dumps_file_path/"
        if not os.path.exists(self.filePath):
            os.makedirs(self.filePath)

    def dumps(self, username):
        user = User._loadByUserName(username)
        company = user.ownCompany
        jsonDict = {"User": [jsonUtils.jsonDoc(user)], "Company":[jsonUtils.jsonDoc(company)]}
        
        for cls in self.clsTypes:
            if cls.__name__ == "User" or cls.__name__ == "Company":
                continue
            objs = company._getRefMeObjects("ownCompany", cls)
            jsonDict[cls.__name__] = jsonUtils.jsonDocList(objs)
        
        f = open(self.filePath+username, "w")
        f.write(json.dumps(jsonDict)+"\n")
        f.close()
        
        
    def _newObj(self, clsName, clsDocList):
        for cls in self.clsTypes:
            if cls.__name__ == clsName:
                for clsDoc in clsDocList:
                    inst = cls()
                    clsDoc["_id"] = xutils.fixObjectId(clsDoc["_id"])
                    inst._medata.update(clsDoc)
                    inst._saveObj()
            
            
    def loads(self, file):
        f = open(self.filePath+file)
        objStr = f.readline()
        jsonDict = json.loads(objStr)
        f.close()
        
        for clsName, clsDocList in jsonDict.items():
            self._newObj(clsName, clsDocList)
            
            

if __name__ == "__main__":
    pass
    


