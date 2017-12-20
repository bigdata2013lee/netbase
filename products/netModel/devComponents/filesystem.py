#coding=utf-8
from products.netModel import medata
from products.netModel.devComponents.base import DeviceComponent

class FileSystem(DeviceComponent):
    dbCollection = 'FileSystem'
    
    def __init__(self, uid=None):
        DeviceComponent.__init__(self)
            
    
    type = medata.plain("type", "NTFS") #分区格式
    blockSize = medata.plain("blockSize", 0) #块大小(字节)
    totalBlocks = medata.plain("totalBlocks", 0) #总块数
    snmpIndex = medata.plain("snmpIndex") #snmp索引
    
    
    @property
    def capacity(self):
        """总容量(字节)"""
        return self.blockSize * self.totalBlocks
    
    @property
    def usedCapacity(self):
        """ 已用(字节) """
        val = self.getPerfValue("FileSystem", "Used", "usedBlocks")
        if val is None: return 0
        
        return val * self.blockSize
        

    def utilization(self):
        "使用率"
        if not self.capacity: return 0
        return self.usedCapacity/self.capacity
    



