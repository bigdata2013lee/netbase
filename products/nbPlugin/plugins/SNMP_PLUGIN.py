#-*- coding:utf-8 -*-
'''
Created on 2013-3-26

@author: Administrator
'''
from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.proto.rfc1902 import ObjectName
from COLLECTBASE import COLLECTBASE
class SNMP_PLUGIN(COLLECTBASE):
    
    def getStartFlag(self):
        return "snmp"
    
    def getValues(self, configsList):
        [self.getValue(oid) for oid in configsList]
        return self.valueDict

    def getValue(self, conf):
        try:
            oid = ObjectName(str(conf).strip())
            iIndication,eStatus,eIndex,vBinds = cmdgen.CommandGenerator().getCmd(
                    cmdgen.CommunityData('my-agent','public',1), 
                    cmdgen.UdpTransportTarget(('192.168.11.22',161)),
                    oid
            )
            for varBind in vBinds:
                name,val = varBind
                self.valueDict[conf] = val.prettyPrint()
        except Exception,e:
            pass
        noneObjList = ['No Such Instance currently exists at this OID','No Such Object currently exists at this OID']
        if not self.valueDict.has_key(conf) or self.valueDict[conf] in noneObjList: 
            self.getTable(conf)
    
    def getTable(self,conf):
        try:
            oid = tuple([int(x) for x in conf.strip(".").split(".")])
            iIndication,eStatus,eIndex,vBinds = cmdgen.CommandGenerator().nextCmd(
                    cmdgen.CommunityData('my-agent','public',1), 
                    cmdgen.UdpTransportTarget(('192.168.11.22',161)),
                    oid
            )
            tmpDict = {}
            for varBind in vBinds:
                for name,val in varBind:
                    tmpDict[name.prettyPrint()] = val.prettyPrint()
            if tmpDict:
                self.valueDict[conf] = tmpDict
        except Exception,e:
            pass
