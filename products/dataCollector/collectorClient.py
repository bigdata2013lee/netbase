#coding=utf-8

from twisted.internet import protocol

from products.dataCollector.baseClient import BaseClient

class CollectorClient(BaseClient, protocol.ClientFactory):
    
    maintainConnection = False 
    cmdindex = 0
    
    def __init__(self, hostname, ip, port, plugins=None, options=None, 
                    device=None, datacollector=None, alog=None):
        """
                初始化函数
        """
        BaseClient.__init__(self, device, datacollector)
        from products.netUtils.Utils import unused
        unused(alog)
        self.hostname = hostname
        self.ip = ip
        self.port = port
        plugins = plugins or []
        self.cmdmap = {}
        self._commands = []
        for plugin in plugins:
            self.cmdmap[plugin.command] = plugin
            self._commands.append(plugin.command)
        self.results = []
        self.protocol = None

        if options:
            defaultUsername = options.username
            defaultPassword = options.password
            defaultLoginTries = options.loginTries
            defaultLoginTimeout = options.loginTimeout
            defaultCommandTimeout = options.commandTimeout
            defaultKeyPath = options.keyPath
            defaultConcurrentSessions = options.concurrentSessions
            defaultSearchPath = options.searchPath
            defaultExistanceTest = options.existenceTest
            
        if device:
            self.username = getattr(device, 
                        'netCommandUsername', defaultUsername)
            self.password = getattr(device, 
                        'netCommandPassword', defaultPassword)
            self.loginTries = getattr(device, 
                        'netCommandLoginTries', defaultLoginTries)
            self.loginTimeout = getattr(device, 
                        'netCommandLoginTimeout', defaultLoginTimeout)
            self.commandTimeout = getattr(device, 
                        'netCommandCommandTimeout', defaultCommandTimeout)
            self.keyPath = getattr(device, 
                        'netKeyPath', defaultKeyPath)
            self.concurrentSessions = getattr(device,
                        'netSshConcurrentSessions', defaultConcurrentSessions)
            self.port = getattr(device, 'netCommandPort', self.port)
            self.searchPath = getattr(device, 
                        'netCommandSearchPath', defaultSearchPath)
            self.existenceTest = getattr(device, 
                        'netCommandExistanceTest', defaultExistanceTest)
        else:
            self.username = defaultUsername
            self.password = defaultPassword
            self.loginTries = defaultLoginTries
            self.loginTimeout = defaultLoginTimeout
            self.commandTimeout = defaultCommandTimeout
            self.keyPath = defaultKeyPath
            self.concurrentSessions = defaultConcurrentSessions
            self.searchPath = defaultSearchPath
            self.existenceTest = defaultExistanceTest


    def addCommand(self, command):
        """
                添加命令
        """
        if isinstance(command, basestring):
            self._commands.append(command)
        else:
            self._commands.extend(command)


    def addResult(self, command, data, exitCode):
        plugin = self.cmdmap.get(command, None)
        self.results.append((plugin, data))

  
    def getCommands(self):
        return self._commands


    def getResults(self):
        return self.results


    def commandsFinished(self):
        return len(self.results) == len(self._commands)


    def clientFinished(self):
        """
                客户端执行完成
        """
        self.cmdindex = 0
        if self.datacollector:
            self.datacollector.clientFinished(self)

    def reinitialize(self):
        """
                重新初始化
        """
        self.cmdmap = {}
        self._commands = []
        self.results = []
