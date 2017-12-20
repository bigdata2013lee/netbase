#! /usr/bin/env python
#coding=utf-8
###########################################################################
#
#
#此软件版权为深圳商之杰科技有限公司所有,更多信息请访问www.netbase.asia
#
#
###########################################################################

__doc__ = """syslog处理类
"""

import re
import socket
from products.netLog.syslog_h import *
from products.netUtils.IpUtil import isip
from products.dataCollector.redisManager import RedisManager

parsers = (
# generic mark
r"^(?P<message>-- (?P<eventClassKey>MARK) --)",

# Cisco UCS
# : 2010 Oct 19 15:47:45 CDT: snmpd: SNMP Operation (GET) failed. Reason:2 reqId (257790979) errno (42) error index (1)
r'^: \d{4} \w{3}\s+\d{1,2}\s+\d{1,2}:\d\d:\d\d \w{3}: (?P<eventClassKey>[^:]+): (?P<message>.*)',

# ntsyslog windows msg
r"^(?P<component>.+)\[(?P<ntseverity>\D+)\] (?P<ntevid>\d+) (?P<message>.*)",

# cisco msg with card indicator
r"%CARD-\S+:(SLOT\d+) %(?P<eventClassKey>\S+): (?P<message>.*)",

# cisco standard msg
r"%(?P<eventClassKey>(?P<component>\S+)-\d-\S+): *(?P<message>.*)",

# Cisco ACS
r"^(?P<ipAddress>\S+)\s+(?P<message>(?P<eventClassKey>CisACS_\d\d_\S+)\s+(?P<eventKey>\S+)\s.*)",

# netscreen device msg
r"device_id=\S+\s+\[\S+\](?P<eventClassKey>\S+\d+):\s+(?P<message>.*)\s+\((?P<originalTime>\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d)\)",

# NetApp
# [deviceName: 10/100/1000/e1a:warning]: Client 10.0.0.101 (xid 4251521131) is trying to access an unexported mount (fileid 64, snapid 0, generation 6111516 and flags 0x0 on volume 0xc97d89a [No volume name available])
r"^\[[^:]+: (?P<component>[^:]+)[^\]]+\]: (?P<message>.*)",

# unix syslog with pid
r"(?P<component>\S+)\[(?P<pid>\d+)\]:\s*(?P<message>.*)",

# unix syslog without pid
r"(?P<component>\S+): (?P<message>.*)",

# adtran devices
r"^(?P<deviceModel>[^\[]+)\[(?P<deviceManufacturer>ADTRAN)\]:(?P<component>[^\|]+\|\d+\|\d+)\|(?P<message>.*)",

r"^date=.+ (?P<message>devname=.+ log_id=(?P<eventClassKey>\d+) type=(?P<component>\S+).+)",

# proprietary message passing system
r"^(?P<component>\S+)(\.|\s)[A-Z]{3} \d \S+ \d\d:\d\d:\d\d-\d\d:\d\d:\d\d \d{5} \d{2} \d{5} \S+ \d{4} \d{3,5} (- )*(?P<message>.*) \d{4} \d{4}",

# Cisco port state logging info
r"^Process (?P<process_id>\d+), Nbr (?P<device>\d+\.\d+\.\d+\.\d+) on (?P<interface>\w+/\d+) from (?P<start_state>\w+) to (?P<end_state>\w+), (?P<message>.+)",

# Cisco VPN Concentrator
# 54884 05/25/2009 13:41:14.060 SEV=3 HTTP/42 RPT=4623 Error on socket accept.
r"^\d+ \d+\/\d+\/\d+ \d+:\d+:\d+\.\d+ SEV=\d+ (?P<eventClassKey>\S+) RPT=\d+ (?P<message>.*)",

# Dell Storage Array
# 2626:48:VolExec:27-Aug-2009 13:15:58.072049:VE_VolSetWorker.hh:75:WARNING:43.3.2:Volume volumeName has reached 96 percent of its reported size and is currently using 492690MB.
r'^\d+:\d+:(?P<component>[^:]+):\d+-\w{3}-\d{4} \d{2}:\d{2}:\d{2}\.\d+:[^:]+:\d+:\w+:(?P<eventClassKey>[^:]+):(?P<message>.*)',

# 1-Oct-2009 23:00:00.383809:snapshotDelete.cc:290:INFO:8.2.5:Successfully deleted snapshot 'UNVSQLCLUSTERTEMPDB-2009-09-30-23:00:14.11563'.
r'^\d+-\w{3}-\d{4} \d{2}:\d{2}:\d{2}\.\d+:[^:]+:\d+:\w+:(?P<eventClassKey>[^:]+):(?P<message>.*)',
) 

# compile regex parsers on load
compiledParsers = []
for regex in parsers:
    keepEntry = True
    if isinstance(regex, tuple):
        regex, keepEntry = regex
    try:
        compiled = re.compile(regex)
        compiledParsers.append((compiled, keepEntry)) 
    except:
        pass


class SyslogProcessor(RedisManager):
    """
    功能:syslog处理类
    作者:wl
    时间:2013.3.13
    """

    def __init__(self,minpriority,parsehost,monitor,defaultPriority,status): 
        """
        功能:初始化
        作者:wl
        时间:2013.3.13
        """
        self.minpriority = minpriority
        self.parsehost = parsehost
        self.monitor = monitor
        self.defaultPriority = defaultPriority
        self.status=status


    def process(self, msg, ipaddr, host, rtime):
        """
        功能:处理syslog,并将其转化成事件格式
        作者:wl
        时间:2013.3.13
        """
        evt = dict(device=host,
                   ipAddress=ipaddr,
                   firstTime=rtime,
                   lastTime=rtime,
                   eventGroup='syslog')
        
        evt, msg = self.parsePRI(evt, msg) 
        if evt['priority'] > self.minpriority: return

        evt, msg = self.parseHEADER(evt, msg, ipaddr)
        evt = self.parseTag(evt, msg) 
        self.status.add(rtime)
        if evt:
            evt = self.buildEventKey(evt)
            evt['monitor'] = self.monitor
            evt['collector'] = "main"
            evt['agent'] = "nbsyslog"
            self.saveEvent(evt)

        
    def parsePRI(self, evt, msg):
        """
                功能:优先级数据解析
                作者:wl
                时间:2013.3.13
        """
        pri = self.defaultPriority
        fac = None
        if msg[:1] == '<':
            pos = msg.find('>')
            fac, pri = LOG_UNPACK(int(msg[1:pos]))
            msg = msg[pos+1:]
        elif msg and msg[0] < ' ':
            fac, pri = LOG_KERN, ord(msg[0])
            msg = msg[1:]
        evt['facility'] = fac
        evt['priority'] = pri
        evt['severity'] = self.defaultSeverityMap(pri)
        return evt, msg


    def defaultSeverityMap(self, pri):
        """
        功能:默认规则对应关系函数
        作者:wl
        时间:2013.3.13
        """
        sev = 1
        if pri < 3: sev = 5
        elif pri == 3: sev = 4
        elif pri == 4: sev = 3
        elif pri == 5 or pri == 6: sev = 2
        return sev


    timeParse = \
        re.compile("^(\S{3} [\d ]{2} [\d ]{2}:[\d ]{2}:[\d ]{2}(?:\.\d{1,3})?) (.*)").search
    notHostSearch = re.compile("[\[:]").search
    def parseHEADER(self, evt, msg, ipaddr):
        """
        功能:syslog头数据解析
        作者:wl
        时间:2013.3.13
        """
        m = re.sub("Kiwi_Syslog_Daemon \d+: \d+: "
            "\S{3} [\d ]{2} [\d ]{2}:[\d ]{2}:[^:]+: ", "", msg)
        m = self.timeParse(msg)
        if m: 
            evt['originalTime'] = m.group(1)
            msg = m.group(2).strip()
        msglist = msg.split()
        if self.parsehost and not self.notHostSearch(msglist[0]):
            device = msglist[0]
            if device.find('@') >= 0:
                device = device.split('@', 1)[1]
            msg = " ".join(msglist[1:])
            evt['device'] = device
            if isip(device):
                evt['ipAddress'] = device
        return evt, msg


    def parseTag(self, evt, msg):
        """
                功能:syslog内容数据解析
                作者:wl
                时间:2013.3.13
        """
        for parser, keepEntry in compiledParsers:    
            m = parser.search(msg)
            if not m:
                continue
            elif not keepEntry:
                return None
        
            evt.update(m.groupdict())
            break
        else:
            evt['message'] = msg
        return evt