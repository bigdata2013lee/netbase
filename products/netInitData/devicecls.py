#coding=utf-8
from products.netModel.org.deviceClass import DeviceClass

def initDeviceClass():
    #DeviceClass(uname, title)
    root = DeviceClass("devicecls", "主机")
    root.__extMedata__({"_id":"devicecls"})
    root._saveObj()
    
    linux = DeviceClass("linux","Linux")
    linux.__extMedata__({"_id":"linux"})
    linux._saveObj()
    
    windows = DeviceClass("windows","Windows")
    windows.__extMedata__({"_id":"windows"})
    windows._saveObj()
           
           
    
    root.addChild(linux).addChild(windows)
    
    
    
if __name__ == '__main__':
    initDeviceClass()
        