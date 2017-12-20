#coding=utf-8
###########################################################################
#       
#
#此软件版权为深圳商之杰科技有限公司所有,更多信息请访问www.netbase.asia
#
#
###########################################################################


__doc__ = """SSH客户端类
See http://twistedmatrix.com/trac/wiki/Documentation for Twisted documentation,
specifically documentation on 'conch' (Twisted's SSH protocol support).
"""

import os
import socket
from pprint import pformat
from twisted.conch.ssh import transport,userauth,connection
from twisted.conch.ssh import common,channel
from twisted.conch.ssh.keys import Key
from twisted.internet import defer,reactor
from products.dataCollector.collectorClient import CollectorClient
import logging
log = logging.getLogger("netcommand")

def sendEvent(self,message = "",device = '',severity = "Error",event_key = None):
    log.info(message)

class SshClientError(Exception):
    """
    异常类
    """

class SshClientTransport(transport.SSHClientTransport):
    """
    SSH客户端传输
    """

    def verifyHostKey(self,hostKey,fingerprint):
        """
                验证主机密钥
        """
        from products.netUtils.Utils import unused
        unused(hostKey)
        return defer.succeed(1)

    def connectionMade(self):
        self.factory.transport = self.transport
        transport.SSHClientTransport.connectionMade(self)

    def receiveError(self,reasonCode,description):
        """
                接收错误信息
        """
        message = 'SSH错误信息(code %d): %s\n' % \
                 (reasonCode,str(description))
        log.warn(message)
        sendEvent(self,message = message)
        transport.SSHClientTransport.receiveError(self,reasonCode,description)

    def receiveUnimplemented(self,seqnum):
        """
                接收未实现的信息
        """
        message = "得到未实现的信息"
        sendEvent(self,message = message)
        transport.SSHClientTransport.receiveUnimplemented(self,seqnum)

    def receiveDebug(self,alwaysDisplay,message,lang):
        """
                接收debug信息
        """
        sendEvent(self,message = message,severity = "Debug")
        transport.SSHClientTransport.receiveDebug(self,alwaysDisplay,message,lang)

    def connectionSecure(self):
        """
                安全连接
        """
        sshconn = SshConnection(self.factory)
        sshauth = SshUserAuth(self.factory.username,sshconn,self.factory)
        self.requestService(sshauth)

class NoPasswordException(Exception):
    pass

class SshUserAuth(userauth.SSHUserAuthClient):
    """
    SSH用户认证
    """

    def __init__(self,user,instance,factory):
        """
                初始化函数
        """
        user = str(user)                # damn unicode
        if user == '':
            import pwd
            try:
                user = os.environ.get('LOGNAME',pwd.getpwuid(os.getuid())[0])
            except:
                pass
            if user == '':
                message = "用户不存在!"
                log.error(message)
                sendEvent(self,message = message)
                self.factory.datacollector.transportWrite({"message":"warn:%s"%message,"data":[]})
                raise SshClientError(message)

        userauth.SSHUserAuthClient.__init__(self,user,instance)
        self._sent_password = False
        self._sent_pk = False
        self._sent_kbint = False
        self._auth_failures = []
        self._auth_succeeded = False
        self.user = user
        self.factory = factory
        self._key = self._getKey()

    def getPassword(self,unused = None):
        """
                得到密码
        """
        if self._sent_password:
            return None
        try:
            password = self._getPassword()
            d = defer.succeed(password)
            self._sent_password = True
        except NoPasswordException,e:
            d = None
        return d

    def getGenericAnswers(self,name,instruction,prompts):
        """
                得到通用的应答
        """
        if not prompts:
            d = defer.succeed([])
        else:
            responses = []
            found_prompt = False
            for prompt,echo in prompts:
                if 'password' in prompt.lower():
                    found_prompt = True
                    try:
                        responses.append(self._getPassword())
                    except NoPasswordException:
                        pass
            if not found_prompt:
                log.warning('未知的提示: %s' % pformat(prompts))
            d = defer.succeed(responses)
        return d

    def _getPassword(self):
        """
                得到密码
        """
        if not self.factory.password:
            message = "密码不存在"
            self.factory.datacollector.transportWrite({"message":"warn:%s"%message,"data":[]})
            raise NoPasswordException(message)
        return self.factory.password

    def _handleFailure(self,message,event_key = None):
        log.error(message)
        sendEvent(self,message = message,event_key = event_key)

    def _getKey(self):
        """
                得到SSH键
        """
        keyPath = os.path.expanduser(self.factory.keyPath)
        key = None
        if os.path.exists(keyPath):
            try:
                data = ''.join(open(keyPath).readlines()).strip()
                key = Key.fromString(data,
                               passphrase = self.factory.password)
            except IOError,ex:
                message = "无法读取SSH键"
                log.warn(message)
                device = 'localhost'
                try:
                    device = socket.getfqdn()
                except:
                    pass
                sendEvent(self,device = device,message = message,
                          severity = "Warning")
        else:
            log.debug("SSH键%s不存在" % keyPath)
        return key

    def getPublicKey(self):
        """
                得到SSH公开的键
        """
        if self._key is not None and not self._sent_pk:
            self._sent_pk = True
            return self._key.blob()

    def getPrivateKey(self):
        """
            得到SSH私有的键
        """
        if self._key is None:
            keyObject = None
        else:
            keyObject = self._key.keyObject
        return defer.succeed(keyObject)

    def auth_keyboard_interactive(self,*args,**kwargs):
        print args,kwargs
        if self._sent_kbint:
            return False
        try:
            self._getPassword()
            self._sent_kbint = True
            return userauth.SSHUserAuthClient.auth_keyboard_interactive(self,*args,**kwargs)
        except NoPasswordException:
            return False

    def ssh_USERAUTH_FAILURE(self,*args,**kwargs):
        if self.lastAuth != 'none' and self.lastAuth not in self._auth_failures:
            self._auth_failures.append(self.lastAuth)
        return userauth.SSHUserAuthClient.ssh_USERAUTH_FAILURE(self,*args,**kwargs)

    def ssh_USERAUTH_SUCCESS(self,*args,**kwargs):
        self._auth_succeeded = True
        return userauth.SSHUserAuthClient.ssh_USERAUTH_SUCCESS(self,*args,**kwargs)

    def serviceStopped(self,*args,**kwargs):
        if not self._auth_succeeded:
            if self._auth_failures:
                msg = "SSH通过%s登陆设备%s失败"% (self.user,self.factory.hostname)
                self.factory.datacollector.transportWrite({"message":"warn:%s"%msg,"data":[]})
            else:
                msg = "SSH验证失败!"
                self.factory.datacollector.transportWrite({"message":"warn:%s"%msg,"data":[]})
            self._handleFailure(msg,event_key = "sshClientAuth")
            self.factory.clientFinished()
        return userauth.SSHUserAuthClient.serviceStopped(self,*args,**kwargs)

class SshConnection(connection.SSHConnection):
    """
    SSH连接
    """
    def __init__(self,factory):
        """
                初始化函数
        """
        log.debug("创建一个新的SSH连接...")
        connection.SSHConnection.__init__(self)
        self.factory = factory

    def ssh_CHANNEL_FAILURE(self,packet):
        """
        SSH认证失败
        """
        message = "SSH认证失败"
        self.factory.datacollector.transportWrite({"message":"warn:%s"%message,"data":[]})
        sendEvent(self,message = message)
        connection.SSHConnection.ssh_CHANNEL_FAILURE(self,packet)

    def ssh_CHANNEL_OPEN_FAILURE(self,packet):
        """
        SSH通道打开失败
        """
        message = "SSH通道打开失败"
        self.factory.datacollector.transportWrite({"message":"warn:%s"%message,"data":[]})
        sendEvent(self,message = message)
        connection.SSHConnection.ssh_CHANNEL_OPEN_FAILURE(self,packet)

    def ssh_REQUEST_FAILURE(self,packet):
        """
        SSH请求失败
        """
        message = "SSH请求失败"
        sendEvent(self,message = message)
        self.factory.datacollector.transportWrite({"message":"warn:%s"%message,"data":[]})
        connection.SSHConnection.ssh_REQUEST_FAILURE(self,packet)

    def openFailed(self,reason):
        """
                打开失败
        """
        message = "SSH连接失败!"
        sendEvent(self,message = message)
        self.factory.datacollector.transportWrite({"message":"warn:%s"%message,"data":[]})
        connection.SSHConnection.openFailed(self,reason)

    def serviceStarted(self):
        """
                开始
        """
        self.factory.serviceStarted(self)

    def addCommand(self,cmd):
        """
                为每一个命令打开通道
        """
        ch = CommandChannel(cmd,conn = self)
        self.openChannel(ch)

    def channelClosed(self,channel):
        """
            通道关闭
        """
        self.localToRemoteChannel[channel.id] = None
        self.channelsToRemoteChannel[channel] = None
        connection.SSHConnection.channelClosed(self,channel)

class CommandChannel(channel.SSHChannel):
    """
        命令通道
    """
    name = 'session'
    conn = None

    def __init__(self,command,conn = None):
        """
                初始化函数
        """
        channel.SSHChannel.__init__(self,conn = conn)
        self.command = command
        self.exitCode = None

    @property
    def targetIp(self):
        if self.conn:
            return self.conn.transport.transport.addr[0]

    def openFailed(self,reason):
        """
                打开失败
        """
        from twisted.conch.error import ConchError
        if isinstance(reason,ConchError):
            args = (reason.data,reason.value)
        else:
            args = (reason.code,reason.desc)
        message = '通道打开失败(error code %d): %s' % (
                (self.command,) + args)
        log.warn("%s %s" % (self.targetIp,message))
        sendEvent(self,message = message)
        channel.SSHChannel.openFailed(self,reason)
        if self.conn is not None:
            self.conn.factory.clientFinished()

    def extReceived(self,dataType,data):
        """
                接收错误数据
        """
        message = '命令%s返回错误信息'%(self.command)
        sendEvent(self,message = message)

    def channelOpen(self,unused):
        """
                打开通道
        """

        self.data = ''
        d = self.conn.sendRequest(self,'exec',common.NS(self.command),
                                  wantReply = 1)
        return d

    def request_exit_status(self,data):
        """
                退出状态
        """
        try:
            import struct
            self.exitCode = struct.unpack('>L',data)[0]
        except:pass

    def dataReceived(self,data):
        """
                接收数据
        """
        self.data += data

    def closed(self):
        """
                关闭通道
        """
        self.conn.factory.addResult(self.command,self.data,self.exitCode)
        self.loseConnection()
        self.conn.factory.channelClosed()

class SshClient(CollectorClient):
    """
    SSH客户端
    """

    def __init__(self,hostname,ip,port = 22,plugins = [],options = None,
                    device = None,datacollector = None,isLoseConnection = False):
        """
        SSH客户端初始化函数
        """
        
        CollectorClient.__init__(self,hostname,ip,port,
                           plugins,options,device,datacollector)
        self.hostname = hostname
        self.protocol = SshClientTransport
        self.connection = None
        self.transport = None
        self.openSessions = 0
        self.workList = list(self.getCommands())
        self.isLoseConnection = isLoseConnection

    def run(self):
        """
                开始连接SSH
        """
        reactor.connectTCP(self.ip,self.port,self,self.loginTimeout)

    def runCommands(self):
        """
                运行命令
        """
        availSessions = self.concurrentSessions - self.openSessions
        for i in xrange(min(len(self.workList),availSessions)):
            cmd = self.workList.pop(0)
            self.openSessions += 1
            self.connection.addCommand(cmd)

    def channelClosed(self):
        """
                关闭通道
        """
        self.openSessions -= 1
        if self.commandsFinished():
            if self.isLoseConnection:
                self.transport.loseConnection()
            self.clientFinished()
            return

        if self.workList:
            cmd = self.workList.pop(0)
            self.openSessions += 1
            if self.connection:
                self.connection.addCommand(cmd)

    def serviceStarted(self,sshconn):
        """
                开始运行
        """
        log.debug("SSH客户端连接到设备%s" % (self.hostname))
        self.connection = sshconn
        self.runCommands()

    def addCommand(self,commands):
        """
                添加命令到队列
        """
        CollectorClient.addCommand(self,commands)
        if isinstance(commands,basestring):
            commands = (commands,)
        self.workList.extend(commands)

        if self.connection:
            self.runCommands()

    def clientConnectionFailed(self,connector,reason):
        """
                连接失败
        """
        from products.netUtils.Utils import unused
        unused(connector)
        message = reason.getErrorMessage()
        log.error("%s %s" % (self.ip,message))
        self.datacollector.transportWrite({"message":"warn:连接%s失败,请查看设备是否开启!"%self.ip,"data":[]})
        sendEvent(self,device = self.hostname,message = message)
        self.clientFinished()

    def loseConnection(self):
        """
                失去连接
        """
        log.debug("%s上的SSH连接关闭" % self.ip)
        #self.connection.loseConnection()
