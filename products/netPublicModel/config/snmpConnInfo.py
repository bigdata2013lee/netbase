#coding=utf-8
ATTRIBUTES = (
    'id',
    'manageIp',
    'netMaxOIDPerRequest',
    'netSnmpMonitorIgnore',
    'netSnmpAuthPassword',
    'netSnmpAuthType',
    'netSnmpCommunity',
    'netSnmpPort',
    'netSnmpPrivPassword',
    'netSnmpPrivType',
    'netSnmpSecurityName',
    'netSnmpTimeout',
    'netSnmpTries',
    'netSnmpVer',
    )

class SnmpConnInfo():
    """
    功能:SNMP连接信息类
    作者:wl
    时间:2013.1.29
    """
    def __init__(self,manageIp,snmpConfig):
        """
        功能:存储属性
        参数:设备IP，设备上的snmpConfig
        作者:wl
        时间:2013.1.29
        """
        for propertyName in ATTRIBUTES:
            setattr(self,propertyName,snmpConfig.get(propertyName,None))
            self.id = manageIp
            self.manageIp = manageIp
            self.netSnmpTries = 2

    def __cmp__(self,other):
        for propertyName in ATTRIBUTES:
            c = cmp(getattr(self,propertyName),getattr(other,propertyName))
            if c != 0:
                return c
        return 0

    def summary(self):
        result = 'SNMP info for %s at %s:%s' % (
            self.id,self.manageIp,self.netSnmpPort)
        result += ' timeout: %s tries: %d' % (
            self.netSnmpTimeout,self.netSnmpTries)
        result += ' version: %s ' % (self.netSnmpVer)
        if '3' not in self.netSnmpVer:
            result += ' community: %s' % self.netSnmpCommunity
        else:
            result += ' securityName: %s' % self.netSnmpSecurityName
            result += ' authType: %s' % self.netSnmpAuthType
            result += ' privType: %s' % self.netSnmpPrivType
        return result

    def createSession(self,protocol = None,allowCache = False):
        """
        功能:基于SNMP的属性创建SNMP的连接会话
        参数:
        作者:wl
        时间:2013.1.29
        """
        from pynetsnmp.twistedsnmp import AgentProxy
        cmdLineArgs = []
        if '3' in self.netSnmpVer:
            if self.netSnmpPrivType:
                cmdLineArgs += ['-l','authPriv']
                cmdLineArgs += ['-x',self.netSnmpPrivType]
                cmdLineArgs += ['-X',self.netSnmpPrivPassword]
            elif self.netSnmpAuthType:
                cmdLineArgs += ['-l','authNoPriv']
            else:
                cmdLineArgs += ['-l','noAuthNoPriv']
            if self.netSnmpAuthType:
                cmdLineArgs += ['-a',self.netSnmpAuthType]
                cmdLineArgs += ['-A',self.netSnmpAuthPassword]
            cmdLineArgs += ['-u',self.netSnmpSecurityName]
        p = AgentProxy(ip = self.manageIp,
                       port = self.netSnmpPort,
                       timeout = self.netSnmpTimeout,
                       snmpVersion = self.netSnmpVer,
                       community = self.netSnmpCommunity,
                       cmdLineArgs = cmdLineArgs,
                       protocol = protocol,
                       allowCache = allowCache)
        p.snmpConnInfo = self
        return p

    def __repr__(self):
        return '<%s for %s>' % (self.__class__,self.id)
