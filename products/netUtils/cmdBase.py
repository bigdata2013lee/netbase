#coding=utf-8
import os
import sys
from products.netUtils.xutils import nbPath as _p
reload(sys)
sys.setdefaultencoding("utf-8")
from optparse import OptionParser
import logging
from logging import handlers

UMASK = 0022
WORKDIR = "/"
MAXFD = 3 

if (hasattr(os, "devnull")):
    REDIRECT_TO = os.devnull
else:
    REDIRECT_TO = "/dev/null"

class CmdBase(object):
    """
    命令行参数基类
    """
    def __init__(self):
        """
        初始化参数设置
        """
        self.parser = None
        self.buildOptions()
        self.parseOptions()
        self.setupLogging()
        if self.options.daemon:
            self.becomeDaemon()
            if self.options.daemon:
                try:
                    self.writePidFile()
                except OSError:
                    msg= "错误: 无法打开PID文件%s" % \
                                    (self.pidfile or '(unknown)')
                    raise SystemExit(msg)
        
    def writePidFile(self):
        """
        写PID文件
        """
        myname = sys.argv[0].split(os.sep)[-1]
        if myname.endswith('.py'): myname = myname[:-3]
        if myname.endswith('.pyc'): myname = myname[:-4]
        myname = "%s.pid" % (myname)
        self.pidfile =_p("/bin/netpid/%s"%myname)
        fp = open(self.pidfile, 'w')
        fp.write(str(os.getpid()))
        self.renicePid(os.getpid())
        fp.close()
        
    
    def renicePid(self,pid):
        """
        调整nice值
        """
        try:
            os.system("renice -20 %s"%pid)
        except Exception,e:
            print "调整nice值失败!"
        
    def becomeDaemon(self):
        """
        守护进程
        """
        try:
            pid = os.fork()
        except OSError, e:
            raise Exception( "%s [%d]" % (e.strerror, e.errno) )

        if (pid == 0):
            os.setsid()
            try:
                pid = os.fork()
            except OSError, e:
                raise Exception( "%s [%d]" % (e.strerror, e.errno) )

            if (pid == 0):
                os.chdir(WORKDIR)
                os.umask(UMASK)
            else:
                os._exit(0)
        else:
            os._exit(0)

        for fd in xrange(0, MAXFD):
            try:
                os.close(fd)
            except OSError:
                pass
        os.open(REDIRECT_TO, os.O_RDWR)
        os.dup2(0, 1)
        os.dup2(0, 2)


    def sigTerm(self, signum=None, frame=None):
        """
        打断
        """
        stop = getattr(self, "stop", None)
        if callable(stop): stop()
        if self.pidfile and os.path.exists(self.pidfile):
            self.log.info("Deleting PID file %s ...", self.pidfile)
            os.remove(self.pidfile)
        self.log.info('守护进程 %s 关闭' % self.__class__.__name__)
        raise SystemExit
    
    def checkLogpath(self):
        """
        检查日志文件的写入路径是否正确
        """
        if not self.options.logpath:
                return None
        else:
            logdir = self.options.logpath
            if not os.path.exists(logdir):
                try:
                    os.makedirs(logdir)
                except OSError, ex:
                    raise SystemExit("文件路径创建失败!" % logdir)
            elif not os.path.isdir(logdir):
                raise SystemExit("文件路径不是一个文件夹!" % logdir)
            return logdir
        
    def setupLogging(self):
        """
        设置日志选项
        """
        rlog = logging.getLogger()
        rlog.setLevel(logging.INFO)
        mname = self.__class__.__name__
        self.log = logging.getLogger("net"+ mname)
        nlog = logging.getLogger("net")
        nlog.setLevel(self.options.logseverity)
        if self.options.daemon:
            logdir = self.checkLogpath()
            if logdir:
                logfile = os.path.join(logdir, mname.lower()+".log")
                maxBytes = self.options.maxLogKiloBytes * 1024
                backupCount = self.options.maxBackupLogs
                h = logging.handlers.RotatingFileHandler(logfile,'a',maxBytes, backupCount)
                h.setFormatter(logging.Formatter(
                    "%(asctime)s %(levelname)s %(name)s: %(message)s",
                    "%Y-%m-%d %H:%M:%S"))
                rlog.addHandler(h)
        else:
                logging.basicConfig()
                f = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
                [ h.setFormatter(f) for h in rlog.handlers ]
        
    def buildOptions(self):
        """
        功能:命令行参数
        作者:wl
        时间:2013.3.13
        """
        if not self.parser:
            self.parser = OptionParser()
        self.parser.add_option('--configfilepath',dest='configfilepath',
                               default=_p('/etc'),
                               help='配置文件存放目录,默认为$NBHOME/etc')
        self.parser.add_option('-D', '--daemon', default=False,
                dest='daemon',action="store_true",
                help="后台运行")
        self.parser.add_option('-v', '--logseverity',dest='logseverity',
                        default=20,type='int',
                        help='日志级别')
        self.parser.add_option('--logpath',dest='logpath',
                        help='日志文件路径', default=_p('/log'))
        self.parser.add_option('--maxlogsize',dest='maxLogKiloBytes',
                        help='日志文件最大容量',
                        default=10240,type='int')
        self.parser.add_option('--maxbackuplogs',dest='maxBackupLogs',
                        help='备份的日志文件最大数',default=3,type='int')
    
    def parseOptions(self):
        """
        解析命令执行的选项
        """
        args = sys.argv[1:]
        (self.options, self.args) = self.parser.parse_args(args=args)
        
if __name__ == "__main__":
    CmdBase()
