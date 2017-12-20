#coding=utf-8
###########################################################################
#
#
#此软件版权为深圳商之杰科技有限公司所有,更多信息请访问www.netbase.cc
#
#
###########################################################################

import sys
import os
import time
import socket
import ip
import icmp
import errno
import logging
from twisted.internet import reactor,defer
log = logging.getLogger("netPing")

class PermissionError(Exception):
    """权限异常类"""

class IpConflict(Exception):
    """相同IP异常类"""

class PingJob():
    """
        构建Ping设备实体对象
        作者:wl
        时间:2013-1-22
    """
    def __init__(self,pingConfig):
        self.parent = False
        self.ipaddr = pingConfig.deviceIp
        self.hcPort = pingConfig.devicePort
        self.hcType = pingConfig.hcType
        self.deviceId = pingConfig.deviceId
        self.title = pingConfig.title
        self.cuid=pingConfig.cuid
        self.componentType = pingConfig.componentType
        self.reset()

    def reset(self):
        self.deferred = defer.Deferred()
        self.rrt = 0
        self.start = 0
        self.sent = 0
        self.message = ""
        self.severity = 5
        self.inprocess = False
        self.pathcheck = 0
        self.eventState = 0

class Ping(object):
    """
    功能:异步Ping类
    作者:wl
    时间:2013-1-25
    """
    def __init__(self,tries = 2,timeout = 1,sock = None):
        """
        功能:ping初始化方法
        作者:wl
        时间:2013-1-25
        """
        self.reconfigure(tries,timeout)
        self.procId = os.getpid()
        self.jobqueue = {}
        self.pktdata = 'netping %s %s' % (socket.getfqdn(),self.procId)
        self.createPingSocket(sock)

    def reconfigure(self,tries = 2,timeout = 3):
        self.tries = tries
        self.timeout = timeout


    def createPingSocket(self,sock):
        """
        功能:创建PING包并接受返回结果
        作者:wl
        时间:2013-1-22
        """
        socketargs = socket.AF_INET,socket.SOCK_RAW,socket.IPPROTO_ICMP
        if sock is None:
            try:
                self.pingsocket = socket.socket(*socketargs)
            except socket.error,e:
                err,msg = e.args
                if err == errno.EACCES:
                    raise PermissionError("必须是root权限")
                raise e
        else:
            self.pingsocket = socket.fromfd(sock,*socketargs)
            os.close(sock)
        self.pingsocket.setblocking(0)
        reactor.addReader(self)

    def fileno(self):
        return self.pingsocket.fileno()

    def doRead(self):
        """
        功能:读取ICMP数据包
        作者:wl
        时间:2013-1-22
        """
        self.recvPackets()

    def connectionLost(self,unused):
        """
        功能:关闭连接
        作者:wl
        时间:2013-1-22
        """
        reactor.removeReader(self)
        self.pingsocket.close()

    def logPrefix(self):
        return None

    def sendPacket(self,pingJob):
        """
        功能:发送ICMP包
        作者:wl
        时间:2013-1-22
        """
        if pingJob.hcType != "ping":
            self.checkPort(pingJob)
        else:
            try:
                pkt = icmp.Echo(self.procId,pingJob.sent,self.pktdata)
                buf = icmp.assemble(pkt)
                pingJob.start = time.time()
#                log.info("发送icmp到 '%s'", pingJob.ipaddr)
                self.pingsocket.sendto(buf,(pingJob.ipaddr,0))
                reactor.callLater(self.timeout,self.checkTimeout,pingJob)
                pingJob.sent += 1
                current = self.jobqueue.get(pingJob.deviceId,None)
                if current:
                    if pingJob.ipaddr != current.ipaddr:
                        raise IpConflict("设备%s 和 %s 用相同的ip %s" %
                                         (pingJob.ipaddr,
                                          current.ipaddr,
                                          pingJob.ipaddr))
                self.jobqueue[pingJob.deviceId] = pingJob
            except (SystemExit,KeyboardInterrupt): raise
            except Exception,e:
                pingJob.rtt = -1
                pingJob.message = "%s 发生错误 %s" % (pingJob.ipaddr,e)
                self.reportPingJob(pingJob)

    
    def getPingJob(self,rip):
        """
        得到Ping对象的ID
        """
        for jq in self.jobqueue.itervalues():
            if jq.ipaddr==rip:
                return jq.deviceId
        return 0

    def recvPackets(self):
        """
        功能:接受ICMP包并分析
        作者:wl
        时间:2013-1-22
        """
        while reactor.running:
            try:
                data,(host,port) = self.pingsocket.recvfrom(1024)
                if not data: return
                ipreply = ip.disassemble(data)
                try:
                    icmppkt = icmp.disassemble(ipreply.data)
                except ValueError:
                    log.error("checksum failure on packet %r",ipreply.data)
                    try:
                        icmppkt = icmp.disassemble(ipreply.data,0)
                    except ValueError:
                        continue
                except Exception,ex:
                    continue
                sip = ipreply.src
                sdeviceId=self.getPingJob(sip)
                if (icmppkt.get_type() == icmp.ICMP_ECHOREPLY and
                    icmppkt.get_id() == self.procId and sdeviceId):
                    self.pingJobSucceed(self.jobqueue[sdeviceId])
                elif icmppkt.get_type() == icmp.ICMP_UNREACH:
                    try:
                        origpkt = icmppkt.get_embedded_ip()
                        dip = origpkt.dst
                        ddeviceId=self.getPingJob(dip)
                        if (origpkt.data.find(self.pktdata) > -1
                            and ddeviceId):
                            self.pingJobFail(self.jobqueue[ddeviceId])
                    except ValueError,ex:
                        log.error("failed to parse host unreachable packet")
                else:
                    log.info("unexpected pkt %s %s",sip,icmppkt)
                    log.info("设备%s无应答" % sip)
            except (SystemExit,KeyboardInterrupt): raise
            except socket.error,err:
                errnum,errmsg = err.args
                if errnum == errno.EAGAIN:
                    return
                raise err
            except Exception,ex:
                log.exception("receiving packet error: %s" % ex)


    def pingJobSucceed(self,pj):
        """
        功能:成功的PING
        作者:wl
        时间:2013-1-22
        """
        log.info("pingJob succeed for %s",pj.ipaddr)
        pj.rtt = time.time() - pj.start
        pj.message = "ip %s 已启动" % (pj.ipaddr)
        self.reportPingJob(pj)

    def portScanSocket(self,ipaddress,ports):
        """
        功能:端口扫描
        作者:wl
        时间:2013-1-22
        """
        ports = ports.split(",")
        for port in ports:
            if port.isdigit():
                try:
                    s = socket.socket()
                    s.settimeout(self.timeout)
                    status=s.connect_ex((ipaddress,int(port)))
                    if not status:
                        return True
                except:pass
                finally:
                    s.close()
        return False

    def checkPort(self,pj):
        """
        功能:通过端口判断设备健康状态
        作者:wl
        时间:2013-1-22
        """
        ports = pj.hcPort
        ipaddress = pj.ipaddr
        if ports:
            hcPort = self.portScanSocket(ipaddress,ports)
            if hcPort:self.pingJobSucceed(pj)
            else:self.pingJobFail(pj)

    def pingJobFail(self,pj):
        """
        功能:失败的PING
        作者:wl
        时间:2013-1-22
        """
        cmdPing="ping "+pj.ipaddr+" -c 1 -w 3"
        flag=os.system(cmdPing)
        if int(flag)==0:
            pj.rtt = time.time() - pj.start
            pj.message = "ip %s 已启动" % (pj.ipaddr)
        else:
            log.info("pingJob fail for %s",pj.ipaddr)
            pj.rtt = -1
            pj.message = "ip %s 已宕机" % (pj.ipaddr)
        self.reportPingJob(pj)

    def reportPingJob(self,pj):
        """
        功能:PING情况输出
        作者:wl
        时间:2013-1-22
        """
        try:
            del self.jobqueue[pj.deviceId]
        except KeyError:
            pass
        # also free the deferred from further reporting
        if pj.rtt < 0:
            pj.deferred.errback(pj)
        else:
            pj.deferred.callback(pj)


    def checkTimeout(self,pj):
        """
        功能:PING的过程中超时检查
        作者:wl
        时间:2013-1-22
        """
        if self.jobqueue.has_key(pj.deviceId):
            now = time.time()
            if now - pj.start > self.timeout:
                if pj.sent >= self.tries:
#                    log.info("pingJob timeout for %s", pj.ipaddr)
                    self.pingJobFail(pj)
                else:
                    self.sendPacket(pj)
            else:
                log.info("calling checkTimeout needlessly for %s",pj.ipaddr)

    def jobCount(self):
        """
        功能:PING的序列数
        作者:wl
        时间:2013-1-22
        """
        return len(self.jobqueue)

    def ping(self,ip):
        """
        功能:创建PingJob对象,并返回对象执行结果
        作者:wl
        时间:2013-1-22
        """
        pj = PingJob(ip)
        self.sendPacket(pj)
        return pj.deferred


def _printResults(results,start):
    """
    功能:打印结果
    作者:wl
    时间:2013-1-22
    """
    good = [pj for s,pj in results if s and pj.rtt >= 0]
    bad = [pj for s,pj in results if s and pj.rtt < 0]
    reactor.stop()

if __name__ == "__main__":
    ping = Ping()
    if len(sys.argv) > 1: targets = sys.argv[1:]
    else: targets = ("127.0.0.2",)
    lst = defer.DeferredList(map(ping.ping,targets),consumeErrors = True)
    lst.addCallback(_printResults,time.time())
    reactor.run()
