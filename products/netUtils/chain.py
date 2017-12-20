#coding=utf-8
###########################################################################
#
#
#此软件版权为深圳商之杰科技有限公司所有,更多信息请访问www.netbase.asia
#
#
###########################################################################
#! /usr/bin/env python 

__doc__='''Chain

Chain a series of deferred actions serially.

$Id$
'''

__version__ = "$Revision$"[11:-2]

from twisted.internet import defer

class Chain:
    """Call a function over an interable of data, after each finishes."""

    def __init__(self, callable, iterable):
        self.callable = callable
        self.iterable = iterable
        self.results = []
        self.defer = defer.Deferred()

    def run(self):
        self.next()
        return self.defer

    def next(self):
        "run the next step"
        try:
            next = self.iterable.next()
            self.callable(next).addCallbacks(self.success, self.failure)
        except StopIteration:
            self.defer.callback(self.results)
        except Exception, ex:
            self.failure(ex)

    def success(self, result):
        "gather a successful result"
        self.results.append((True, result))
        self.next()

    def failure(self, result):
        "gather an error result"
        self.results.append((False, result))
        self.next()

