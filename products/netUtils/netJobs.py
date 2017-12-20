#! /usr/bin/env python
#coding=utf-8 

from twisted.internet import defer

class NetJobs:
    def __init__(self, max, callable, data):
        self.defer = defer.Deferred()
        self.results = []
        self.max = max
        self.callable = callable
        self.workQueue = data
        self.running = 0

    def start(self):
        self._runSome()
        return self.defer

    def status(self):
        return self.running, len(self.workQueue), len(self.results)

    def _runSome(self):
        while self.running < self.max and self.workQueue:
            self.running += 1
            try:
                d = self.callable(self.workQueue.pop())
            except Exception, ex:
                self._finished(ex)
            else:
                d.addBoth(self._finished)
        if self.running == 0 and not self.workQueue and not self.defer.called:
            self.defer.callback(self.results)

    def _finished(self, result):
        self.running -= 1
        self.results.append(result)
        self._runSome()


