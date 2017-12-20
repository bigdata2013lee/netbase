#coding=utf-8
###########################################################################
#
#
#此软件版权为深圳商之杰科技有限公司所有,更多信息请访问www.netbase.asia
#
#
###########################################################################

__doc__ = """Utils

General utility functions module

"""
import os
import re
import types
import traceback
from twisted.internet import reactor
from twisted.python import failure
def localIpCheck(context,ip):
    """
    Test to see if an IP should not be included in the network map.
    Uses the zLocalIpAddresses to decide.

    @param context: Zope object
    @type context: object
    @param ip: IP address
    @type ip: string
    @return: regular expression match or None (if not found)
    @rtype: re match object
    """
    return re.search(getattr(context,'zLocalIpAddresses','^$'),ip)

def prepId(id, subchar='_'):
    """
    Make an id with valid url characters. Subs [^a-zA-Z0-9-_,.$\(\) ]
    with subchar.  If id then starts with subchar it is removed.

    @param id: user-supplied id
    @type id: string
    @return: valid id
    @rtype: string
    """
    _prepId = re.compile(r'[^a-zA-Z0-9-_,.$\(\) ]').sub
    _cleanend = re.compile(r"%s+$" % subchar).sub
    if id is None: 
        raise ValueError('Ids can not be None')
    if type(id) not in types.StringTypes:
        id = str(id)
    id = _prepId(subchar, id)
    while id.startswith(subchar):
        if len(id) > 1: id = id[1:]
        else: id = "-"
    id = _cleanend("",id)
    id = id.strip()
    return str(id)

def sane_pathjoin(base_path,*args):
    """
    Joins paths in a saner manner than os.path.join()

    @param base_path: base path to assume everything is rooted from
    @type base_path: string
    @param *args: path components starting from $ZENHOME
    @type *args: strings
    @return: sanitized path
    @rtype: string
    """
    path = base_path
    if args:
        # Hugely bizarre (but documented!) behaviour with os.path.join()
        # >>> import os.path
        # >>> os.path.join( '/blue', 'green' )
        # '/blue/green'
        # >>> os.path.join( '/blue', '/green' )
        # '/green'
        # Work around the brain damage...
        base = args[0]
        if base.startswith(base_path):
            path_args = [ base ] + [a.strip('/') for a in args[1:] if a != '' ]
        else:
            path_args = [a.strip('/') for a in args if a != '' ]

        # Empty strings get thrown out so we may not have anything
        if len(path_args) > 0:
            # What if the user splits up base_path and passes it in?
            pathological_case = os.path.join(*path_args)
            if pathological_case.startswith(base_path):
                pass

            elif not base.startswith(base_path):
                path_args.insert(0,base_path)

            # Note: passing in a list to os.path.join() returns a list,
            #       again completely unlike string join()
            path = os.path.join(*path_args)

    # os.path.join( '/blue', '' ) returns '/blue/' -- egads!
    return path.rstrip('/')


def zenPath(*args):
    """
    Return a path relative to $ZENHOME specified by joining args.  The path
    is not guaranteed to exist on the filesystem.
    
    >>> import os
    >>> zenHome = os.environ['ZENHOME']
    >>> zenPath() == zenHome
    True
    >>> zenPath( '' ) == zenHome
    True
    >>> zenPath('Products') == os.path.join(zenHome, 'Products')
    True
    >>> zenPath('/Products/') == zenPath('Products')
    True
    >>> 
    >>> zenPath('Products', 'foo') == zenPath('Products/foo')
    True

    # NB: The following is *NOT* true for os.path.join()
    >>> zenPath('/Products', '/foo') == zenPath('Products/foo')
    True
    >>> zenPath(zenPath('Products')) == zenPath('Products')
    True
    >>> zenPath(zenPath('Products'), 'orange', 'blue' ) == zenPath('Products', 'orange', 'blue' )
    True

    # Pathological case
    # NB: need to expand out the array returned by split()
    >>> zenPath() == zenPath( *'/'.split(zenPath()) )
    True

    @param *args: path components starting from $ZENHOME
    @type *args: strings
    @todo: determine what the correct behaviour should be if $ZENHOME is a symlink!
    """
    zenhome = os.environ.get('ZENHOME','')

    path = sane_pathjoin(zenhome,*args)

    #test if ZENHOME based path exists and if not try bitrock-style path.
    #if neither exists return the ZENHOME-based path
    if not os.path.exists(path):
        brPath = os.path.realpath(os.path.join(zenhome,'..','common'))
        testPath = sane_pathjoin(brPath,*args)
        if(os.path.exists(testPath)):
            path = testPath
    return path

def zopePath(*args):
    """
    Similar to zenPath() except that this constructs a path based on
    ZOPEHOME rather than ZENHOME.  This is useful on the appliance.
    If ZOPEHOME is not defined or is empty then return ''.
    NOTE: A non-empty return value does not guarantee that the path exists,
    just that ZOPEHOME is defined.
    
    >>> import os
    >>> zopeHome = os.environ.setdefault('ZOPEHOME', '/something')
    >>> zopePath('bin') == os.path.join(zopeHome, 'bin')
    True
    >>> zopePath(zopePath('bin')) == zopePath('bin')
    True
    
    @param *args: path components starting from $ZOPEHOME
    @type *args: strings
    """
    zopehome = os.environ.get('ZOPEHOME','')
    return sane_pathjoin(zopehome,*args)


def binPath(fileName):
    """
    Search for the given file in a list of possible locations.  Return
    either the full path to the file or '' if the file was not found.
    
    >>> len(binPath('zenoss')) > 0
    True
    >>> len(binPath('zeoup.py')) > 0
    True
    >>> len(binPath('check_http')) > 0
    True
    >>> binPath('Idontexistreally') == ''
    True

    @param fileName: name of executable
    @type fileName: string
    @return: path to file or '' if not found
    @rtype: string
    """
    # bin and libexec are the usual suspect locations.
    # ../common/bin and ../common/libexec are additional options for bitrock
    # $ZOPEHOME/bin is an additional option for appliance
    for path in (zenPath(d,fileName) for d in (
                'bin','libexec','../common/bin','../common/libexec')):
        if os.path.isfile(path):
            return path
    path = zopePath('bin',fileName)
    if os.path.isfile(path):
        return path
    return ''
EXIT_CODE_MAPPING = {
    0:'成功',
    1:'一般错误',
    2:'滥用shell内建命令',
    126:'无法执行命令, 权限不足或不是一个可执行的命令',
    127:'找不到该命令',
    128:'无效的参数导致退出,退出并返回0-255之间的整数',
    130:'致命错误编号: 2, Control-C终止命令'
}
def getExitMessage(exitCode):
    """
    Return a nice exit message that corresponds to the given exit status code

    @param exitCode: process exit code
    @type exitCode: integer
    @return: human-readable version of the exit code
    @rtype: string
    """
    if exitCode in EXIT_CODE_MAPPING.keys():
        return EXIT_CODE_MAPPING[exitCode]
    elif exitCode >= 255:
        return 'Exit status out of range, exit takes only integer arguments in the range 0-255'
    elif exitCode > 128:
        return 'Fatal error signal: %s' % (exitCode - 128)
    return 'Unknown error code: %s' % exitCode

def unused(*args):
    """
    A no-op function useful for shutting up pychecker

    @param *args: arbitrary arguments
    @type *args: objects
    @return: count of the objects
    @rtype: integer
    """
    return len(args)


class TimeoutError(Exception):
    """
    功能:超时异常类
    作者:wl
    时间:2013-1-7
    """

    def __init__(self,*args):
        Exception.__init__(self)
        self.args = args

def Timeout(deferred,seconds,obj):
    """
    功能:运行命令超时类
    作者:wl
    时间:2013-1-7
    """

    def _timeout(deferred,obj):
        deferred.errback(failure.Failure(TimeoutError(obj)))

    def _cb(arg,timer):
        if not timer.called:
            timer.cancel()
        return arg

    timer = reactor.callLater(seconds,_timeout,deferred,obj)
    deferred.addBoth(_cb,timer)
    return deferred

class RemoteException(Exception):
    "远程异常类"
    def __init__(self, msg, tb):
        Exception.__init__(self, msg)
        self.traceback = tb
    def __str__(self):
        return Exception.__str__(self) + self.traceback
    
def translateError(callable):
    """
    远程调用抛出异常
    """
    def inner(*args, **kw):
        """
        Interior decorator
        """
        try:
            return callable(*args, **kw)
        except Exception, ex:
            raise RemoteException(
                '远程异常: %s: %s' % (ex.__class__, ex),
                traceback.format_exc())
    return inner
