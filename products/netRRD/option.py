#coding=utf-8
###########################################################################
#       
#
#此软件版权为深圳商之杰科技有限公司所有,更多信息请访问www.netbase.asia
#
#
###########################################################################
import logging
class Options:
    """
    功能:将命令行的参数构建成一个类
    作者:wl
    时间:2013-1-7
    """
    loginTries=1
    searchPath=''
    existenceTest=None

    def __init__(self, username, password, loginTimeout, commandTimeout,
            keyPath, concurrentSessions):
        self.username = username
        self.password = password
        self.loginTimeout=loginTimeout
        self.commandTimeout=commandTimeout
        self.keyPath = keyPath
        self.concurrentSessions = concurrentSessions

def buildOptions(parser=None, usage=None):
    """
    Build a list of command-line options we will accept

    @param parser: optparse parser
    @type parser: optparse object
    @param usage: description of how to use the program
    @type usage: string
    @return: optparse parser
    @rtype: optparse object
    """
    #Default option values
    defaultUsername =""
    defaultPassword = ""
    defaultLoginTries = 2
    defaultLoginTimeout = 10
    defaultCommandTimeout = 10 
    defaultKeyPath = '~/.ssh/id_dsa'
    defaultConcurrentSessions = 10
    defaultSearchPath = []
    defaultExistanceTest = 'test -f %s'

    defaultPromptTimeout = 10 
    defaultLoginRegex = 'ogin'
    defaultPasswordRegex = 'assword'

    if not usage:
        usage = "%prog [options] hostname[:port] command"

    if not parser:
        from optparse import OptionParser
        parser = OptionParser(usage=usage, )
  
    parser.add_option('-u', '--user',
                dest='username',
                default=defaultUsername,
                help='Login username')
    parser.add_option('-P', '--password',
                dest='password',
                default=defaultPassword,
                help='Login password')
    parser.add_option('-t', '--loginTries',
                dest='loginTries',
                default=defaultLoginTries,
                type = 'int',
                help='Number of times to attempt to login')
    parser.add_option('-L', '--loginTimeout',
                dest='loginTimeout',
                type = 'float',
                default = defaultLoginTimeout,
                help='Timeout period (secs) to find login expect statments')
    parser.add_option('-T', '--commandTimeout',
                dest='commandTimeout',
                type = 'float',
                default = defaultCommandTimeout,
                help='Timeout period (secs) after issuing a command')
    parser.add_option('-K', '--keyPath',
                dest='keyPath',
                default = defaultKeyPath,
                help='Path to use when looking for SSH keys')
    parser.add_option('-S', '--concurrentSessions',
                dest='concurrentSessions',
                type='int',
                default = defaultConcurrentSessions,
                help='Allowable number of concurrent SSH sessions')
    parser.add_option('-s', '--searchPath',
                dest='searchPath',
                default=defaultSearchPath,
                help='Path to use when looking for commands')
    parser.add_option('-e', '--existenceTest',
                dest='existenceTest',
                default=defaultExistanceTest,
                help='How to check if a command is available or not')
    if not parser.has_option('-v'):
        parser.add_option('-v', '--logseverity',
                    dest='logseverity',
                    default=logging.INFO,
                    type='int',
                    help='Logging severity threshold')
    parser.add_option('-r', '--promptTimeout',
                dest='promptTimeout',
                type = 'float',
                default = defaultPromptTimeout,
                help='Timeout when discovering prompt')
    parser.add_option('-x', '--loginRegex',
                dest='loginRegex',
                default = defaultLoginRegex,
                help='Python regular expression that will find the login prompt')
    parser.add_option('-w', '--passwordRegex',
                dest='passwordRegex',
                default = defaultPasswordRegex,
                help='Python regex that will find the password prompt')
    parser.add_option('--enable',
                dest='enable', action='store_true', default=False,
                help="Enter 'enable' mode on a Cisco device")
    parser.add_option('--termlen',
                dest='termlen', action='store_true', default=False,
                help="Enter 'send terminal length 0' on a Cisco device")
    return parser

def parseOptions(parser, port):
    """
    Command-line option parser

    @param parser: optparse parser
    @type parser: optparse object
    @param port: IP port number to listen on
    @type port: integer
    @return: parsed options
    @rtype: object
    """
    options, args = parser.parse_args()
    options.port = 22
    return options
