#/usr/bin/env python
#-*- coding:utf-8 -*-
import re
from twisted.internet import reactor,defer
from twisted.conch import telnet
from products.dataCollector.collectorClient import CollectorClient
from products.netRRD.option import parseOptions,buildOptions
import logging
log = logging.getLogger("netcommand")

defaultPromptTimeout = 10
defaultLoginRegex = 'ogin'
defaultPasswordRegex = 'assword'
defaultEnable = False
defaultTermLength = False

responseMap = ("WILL","WONT","DO","DONT")

def check(hostname):
    """
    Check to see if a device supports telnet

    @param hostname: name or IP address of device
    @type hostname: string
    @return: whether or not telnet port is available
    @rtype: integer
    @todo: support alternate ports
    """
    from telnetlib import Telnet
    import socket
    try:
        tn = Telnet(hostname)
        tn.close()
        return 1
    except socket.error:
        return 0

class TelnetClient(CollectorClient):
    def __init__(self,hostname,ip,port,commands = [],options = None,
                    device = None,datacollector = None):
        CollectorClient.__init__(self,hostname,ip,port,commands,options,device,datacollector)
        self.protocol = TelnetClientProtocol
        self.modeRegex = {
                    'Command' : '.*',
                    'WasteTime' : '.*',
                    'Done' : '',
                    }
        self.promptPause = 1

        self.promptTimeout = defaultPromptTimeout
        self.loginRegex = defaultLoginRegex
        self.passwordRegex = defaultPasswordRegex
        self.enable = defaultEnable
        self.termlen = defaultTermLength

        self.modeRegex['Login'] = self.loginRegex
        self.modeRegex['Password'] = self.passwordRegex

        self.defers = {}

    def run(self):
        if self.termlen:
            self._commands.insert(0,"terminal length 0")
        reactor.connectTCP(self.ip,self.port,self)

    def command(self,commands):
        CollectorClient.addCommand(commands)
        if self.myprotocol.mode != "Command":
            self.myprotocol.telnet_SendCommand("")

    def clientConnectionFailed(self,connector,reason):
        log.error("clientconnection failed: %s" % reason.getErrorMessage())
        self.clientFinished()

    def clientFinished(self):
        CollectorClient.clientFinished(self)
        self.commands = []
        self.results = []

    def addResult(self,command,data,code):
        CollectorClient.addResult(self,command,data,code)
        d = self.defers.pop(command)
        if not d.called:
            d.callback((data,code))

    def addCommand(self,command):
        d = defer.Deferred()
        self.defers[command] = d
        CollectorClient.addCommand(self,command)
        return d

class TelnetClientProtocol(telnet.Telnet):
    mode = 'Login'
    timeout = 0
    timeoutID = None
    p1 = ""
    p2 = ""
    commandPrompt = ""
    command = ''
    enabled = -1
    scCallLater = None
    bytes = ""
    lastwrite = ''
    result = ''
    buffer = ""

    def connectionMade(self):
        self.factory.myprotocol = self #bogus hack
        self.hostname = self.factory.hostname
        log.info("连接到设备 %s" % self.hostname)
        self.startTimeout(self.factory.loginTimeout,self.loginTimeout)
        self.protocol = telnet.TelnetProtocol()

    def iac_DO(self,feature):
        log.info("Received telnet DO feature %s" % ord(feature))
        if ord(feature) == 1:
            self._iac_response(telnet.WILL,feature)
        else:
            self._iac_response(telnet.WONT,feature)

    def iac_DONT(self,feature):
        log.info("Received telnet DONT feature %s" % ord(feature))
        self._iac_response(telnet.WONT,feature)

    def iac_WILL(self,feature):
        log.info("Received telnet WILL feature %s" % ord(feature))
        # turn off telnet options
        self._iac_response(telnet.DONT,feature)

    def iac_WONT(self,feature):
        log.info("Received telnet WONT feature %s" % ord(feature))
        # turn off telnet options
        self._iac_response(telnet.DONT,feature)

    def _iac_response(self,action,feature):
        log.info("Sending telnet action %s feature %s" % (
                responseMap[ord(action) - 251],ord(feature)))
        self.write(telnet.IAC + action + feature)

    def write(self,data):
        self.lastwrite = data
        self.transport.write(data)

    def processLine(self,line):
        line = re.sub("\r\n|\r","\n",line) #convert \r\n to \n
        #if server is echoing take it out
        if self.lastwrite.startswith(line):
            self.lastwrite = self.lastwrite[len(line):]
            line = ''
        elif line.find(self.lastwrite) == 0:
            line = line[len(self.lastwrite):]
        self.mode = getattr(self,"telnet_" + self.mode)(line)

    def dataReceived(self,data):
        telnet.Telnet.dataReceived(self,data)
        if self.bytes:
            self.processLine(self.bytes)
        self.bytes = ''

    def applicationDataReceived(self,bytes):
        self.bytes += bytes

    def startTimeout(self,timeout = 1,timeoutfunc = None):
        self.cancelTimeout()
        if timeoutfunc is None: timeoutfunc = self.defaultTimeout
        self.timeoutID = reactor.callLater(timeout,timeoutfunc)

    def cancelTimeout(self):
        if self.timeoutID: self.timeoutID.cancel()
        self.timeoutID = None

    def defaultTimeout(self):
        self.transport.loseConnection()
        if self.factory.commandsFinished():
            self.factory.clientFinished()
        regex = self.factory.modeRegex.get(self.mode,"")
        log.error("Dropping connection to %s: " \
            "state '%s' timeout %.1f seconds regex '%s' buffer '%s'" % \
            (self.factory.hostname,self.mode,self.timeout,regex,self.buffer))

    def loginTimeout(self,loginTries = 0):
        if loginTries == 0:
            loginTries = self.factory.loginTries
        elif loginTries == 1:
            self.transport.loseConnection()
            self.factory.clientFinished()
            log.error("登陆到设备 %s 失败" % self.hostname)
            return "Done"
        else:
            self.factory.loginTries -= 1
            return "Login"

    def telnet_Login(self,data):
        log.info('Search for login regex (%s) in (%s) finds: %r' % \
                  (self.factory.loginRegex,data,\
                   re.search(self.factory.loginRegex,data)))
        if not re.search(self.factory.loginRegex,data): # login failed
            return 'Login'
        if not self.factory.loginTries:
            self.transport.loseConnection()
            log.info("Login to %s with username %s failed" % (
                                self.factory.hostname,self.factory.username))
        else:
            self.factory.loginTries -= 1
        self.write(self.factory.username + '\n')
        return 'Password'

    def telnet_Password(self,data):
        log.debug('Search for password regex (%s) in (%s) finds: %r' % \
                  (self.factory.passwordRegex,data,\
                   re.search(self.factory.loginRegex,data)))
        if not re.search(self.factory.passwordRegex,data): # look for pw prompt
            return 'Password'
        self.write(self.factory.password + '\n')
        self.startTimeout(self.factory.promptTimeout)
        return 'FindPrompt'

    def telnet_Enable(self,unused):
        self.write('enable\n')
        self.startTimeout(self.factory.loginTimeout,self.loginTimeout)
        return "Password"

    def telnet_FindPrompt(self,data):
        if not data.strip(): return 'FindPrompt'
        if re.search(self.factory.loginRegex,data): # login failed
            return self.telnet_Login(data)
        self.p1 = data
        if self.p1 == self.p2:
            self.cancelTimeout() # promptTimeout
            self.commandPrompt = self.p1
            log.info("found command prompt '%s'" % self.p1)
            self.factory.modeRegex['Command'] = re.escape(self.p1) + "$"
            self.factory.modeRegex['SendCommand'] = re.escape(self.p1) + "$"
            if self.factory.enable:
                self.factory.enable = False
                # NB: returns Password
                return self.telnet_Enable("")
            else:
                self.scCallLater = reactor.callLater(1.0,
                    self.telnet_SendCommand,"")
                return "ClearPromptData"
        self.p2 = self.p1
        self.p1 = ""
        reactor.callLater(.1,self.write,"\n")
        return 'FindPrompt'

    def telnet_ClearPromptData(self,unused):
        if self.scCallLater: self.scCallLater.cancel()
        self.scCallLater = reactor.callLater(1.0,self.telnet_SendCommand,"")
        return "ClearPromptData"

    def telnet_SendCommand(self,unused):
        if self.scCallLater and self.scCallLater.active():
            self.scCallLater.cancel()
        log.info("sending command '%s'" % self.curCommand())
        self.write(self.curCommand() + '\n')
        self.startTimeout(self.factory.commandTimeout)
        self.mode = 'Command'
        return 'Command'

    def telnet_Command(self,data):
        self.result += data
        if not self.result.endswith(self.commandPrompt):
            log.info("Prompt '%s' not found" % self.commandPrompt)
            log.info("Line ends wth '%s'" % data[-5:])
            self.write("\n")
            return 'Command'
        self.cancelTimeout()
        data,self.result = self.result,''
        log.info("command = %s, %s" % (self.curCommand(),self.factory))
        self.factory.addResult(self.curCommand(),data[0:-len(self.p1)],None)
        self.factory.cmdindex += 1
        if self.factory.commandsFinished():
            self.factory.clientFinished()
            if not self.factory.maintainConnection:
                self.transport.loseConnection()
            return 'Done'
        else:
            # Command
            return self.telnet_SendCommand("")

    def curCommand(self):
        return self.factory._commands[self.factory.cmdindex]

class FakePlugin(object):
    """
    Fake class to provide plugin instances for command-line processing.
    """
    def __init__(self,command = ''):
        self.command = command

    def __repr__(self):
        return "'%s'" % self.command

def commandsToPlugins(commands):
    return [ FakePlugin(cmd) for cmd in commands ]


def main():
    import socket
#    parser = buildOptions()
#    options = parseOptions(parser, 23)
    commands = commandsToPlugins(["get config"])
    client = TelnetClient(socket.gethostname(),
                          "192.168.7.5",23,commands)
    client.run()
#    client.clientFinished = reactor.stop
    reactor.callLater(1,main)

if __name__ == "__main__":
    main()
    reactor.run()
