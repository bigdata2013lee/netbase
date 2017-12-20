#coding=utf-8
###########################################################################
#
#
#此软件版权为深圳商之杰科技有限公司所有,更多信息请访问www.netbase.asia
#
#
###########################################################################

__doc__='''
生成器的延迟调用
'''
from twisted.internet import defer, reactor
from twisted.python import failure

class ShortCircuit:
    def __init__(self, value):
        self.value = value

class Driver:
    """
    运行迭代并返回一个deferred
    """
    def __init__(self):
        self.defer = defer.Deferred()
        self.result = None

    def drive(self, iterable):
        """
        调用一个迭代
        """
        self.iter = iterable
        self._next()
        return self.defer

    def _next(self):
        """
        得到迭代的next值
        """
        try:
            self.iter.next().addBoth(self._finish)
        except StopIteration:
            self.defer.callback(self.result)
        except ShortCircuit, ex:
            self.result = ex.value
            self.defer.callback(self.result)
        except Exception, ex:
            self.defer.errback(failure.Failure(ex))

    def result(self):
        """
        返回迭代的结果
        """
        ex = self.result
        if isinstance(self.result, failure.Failure):
            ex = self.result.value
        if isinstance(ex, Exception):
            raise ex
        return self.result
    next = result                       # historical name for result

    def finish(self, result):
        raise ShortCircuit(result)

    def _finish(self, result):
        """
        存储deferred的结果next()
        """
        self.result = result
        # prevent endless recursion
        reactor.callLater(0, self._next)

def drive(callable):
    '''
    Driver类的调用
    '''
    d = Driver()
    return d.drive(callable(d))

def driveLater(secs, callable):
    """
    下一次调用
    """
    d = defer.Deferred()
    def driveAgain():
        drive(callable).chainDeferred(d)
    reactor.callLater(secs, driveAgain)
    return d

def test():
    lst = []
    def loop(d):
        for i in xrange(10):
            yield defer.succeed(i)
            lst.append(d.next())
    def final(v):
        assert lst[-1] == v
        assert lst == xrange(10)
        def unloop(d):
            yield  defer.fail(ZeroDivisionError('hahaha'))
            d.next()
        def checkError(err):
            assert isinstance(err.value, ZeroDivisionError)
            reactor.stop()
        drive(unloop).addErrback(checkError)
    drive(loop).addCallback(final)

if __name__ == '__main__':
    test()
    reactor.run()
