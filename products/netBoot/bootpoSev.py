#coding=utf-8
from products.netModel.observer import Observer
from products.netModel.device import Device
from products.netPublicModel.userControl import UserControl
from products.netBoot import bootClient
import copy
import json
import time
import pickle

class BootpoSev(Observer):

    def sentPowerUpCmd(self, bp):
        """
                远程开机
        """
        coll = bp.collector
        if not coll:
            print "Warning: Can't find collector while sentting BootpoCmd"
            return "fail"
        
        vars = copy.deepcopy(bp.ipmiConfig)
        vars["uid"] = bp.getUid()
        #vars["manageIp"] = bp.manageIp
        vars["title"] = bp.titleOrUid()
        vars["componentType"] = bp.getComponentType()
        vars["collector"] = coll.getUid()
        params={"powerOn":vars}
        pickleParams = pickle.dumps(params)
        bp.lastSentBootpoCmdTime = time.time()
        rs=bootClient.sendBootpoCmd(coll.host, coll.bootpoPort, pickleParams)
        return rs

    def sentSoftDownCmd(self, bp):
        """
                远程软关机
        """
        coll = bp.collector
        if not coll:
            print "Warning: Can't find collector while sentting SoftDownCmd"
            return "fail"
        vars = copy.deepcopy(bp.ipmiConfig)
        vars["uid"] = bp.getUid()
        #vars["manageIp"] = bp.manageIp
        vars["title"] = bp.titleOrUid()
        vars["componentType"] = bp.getComponentType()
        vars["collector"] = coll.getUid()
        params={"softOff":vars}
        pickleParams = pickle.dumps(params)
        bp.lastSentBootpoCmdTime = time.time()
        rs=bootClient.sendBootpoCmd(coll.host, coll.bootpoPort, pickleParams)
        return rs
    
    def sentPowerDownCmd(self, bp):
        """
                远程硬关机
        """
        coll = bp.collector
        if not coll:
            print "Warning: Can't find collector while sentting SoftDownCmd"
            return "fail"
        vars = copy.deepcopy(bp.ipmiConfig)
        vars["uid"] = bp.getUid()
        #vars["manageIp"] = bp.manageIp
        vars["title"] = bp.titleOrUid()
        vars["componentType"] = bp.getComponentType()
        vars["collector"] = coll.getUid()
        params={"powerOff":vars}
        pickleParams = pickle.dumps(params)
        bp.lastSentBootpoCmdTime = time.time()
        rs=bootClient.sendBootpoCmd(coll.host, coll.bootpoPort, pickleParams)
        return rs
    
    def sentPowerResetCmd(self, bp):
        """
                远程硬重启
        """
        coll = bp.collector
        if not coll:
            print "Warning: Can't find collector while sentting SoftDownCmd"
            return "fail"
        vars = copy.deepcopy(bp.ipmiConfig)
        vars["uid"] = bp.getUid()
        #vars["manageIp"] = bp.manageIp
        vars["title"] = bp.titleOrUid()
        vars["componentType"] = bp.getComponentType()
        vars["collector"] = coll.getUid()
        params={"powerReset":vars}
        pickleParams = pickle.dumps(params)
        bp.lastSentBootpoCmdTime = time.time()
        rs=bootClient.sendBootpoCmd(coll.host, coll.bootpoPort, pickleParams)
        return rs
    
    def getPowerStatus(self,bp):
        """
                获取电源状态
        """
        coll=bp.collector
        if not coll:return "fail"
        vars = copy.deepcopy(bp.ipmiConfig)
        vars["uid"] = bp.getUid()
        #vars["manageIp"] = bp.manageIp
        vars["title"] = bp.titleOrUid()
        vars["componentType"] = bp.getComponentType()
        vars["collector"] = coll.getUid()
        params={"powerStatus":vars}
        pickleParams = pickle.dumps(params)
        bp.lastSentBootpoCmdTime = time.time()
        rs=bootClient.sendBootpoCmd(coll.host, int(coll.bootpoPort), pickleParams)
        return rs
    
        
        
        