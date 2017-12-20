#! /usr/bin/env python 
#coding=utf-8
__doc__="""wmi客户端
得到WMI性能数据.
"""

import re
import socket
from DateTime import DateTime
from twisted.internet import defer, reactor
from twisted.python.failure import Failure

from pysamba.twisted.callback import WMIFailure
from products.netRRD.wmiQuery import Query
from products.netUtils.driver import drive
from products.dataCollector.baseClient import BaseClient
import logging
log = logging.getLogger("wmiClient")

DTPAT=re.compile(r'^(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})\.(\d{6})([+|-])(\d{3})')

class BadCredentials(Exception): pass

def sortQuery(qs, table, query):
    
    cn, kbs, ns, props = query
    if not kbs: kbs = {}
    ikey = tuple(kbs.keys())
    ival = tuple(kbs.values())
    try:
        if ival not in qs[ns][cn][ikey]:
            qs[ns][cn][ikey][ival] = []
        qs[ns][cn][ikey][ival].append((table, props))
    except KeyError:
        try:
            qs[ns][cn][ikey] = {}
        except KeyError:
            try:
                qs[ns][cn] = {}
            except KeyError:
                qs[ns] = {}
                qs[ns][cn] = {}
            qs[ns][cn][ikey] = {}
        qs[ns][cn][ikey][ival] = [(table, props)]
    return qs

class WMIClient(BaseClient):

    def __init__(self, device, datacollector=None, plugins=[]):
        BaseClient.__init__(self, device, datacollector)
        self.device = device
        self.host = device.manageIp
        self._wmipool = {}
        if device.wmiProxy is not "":
            self.host = device.wmiProxy
        elif socket.getfqdn().lower() == device.manageIp.lower(): 
            self.host = "."
            device.winUser = device.winPassword = ""
        elif device.manageIp is not "":
            self.host = device.manageIp
        self.name = device.manageIp
        self.user = device.winUser
        self.passwd = device.winPassword
        self.datacollector = datacollector
        self.plugins = plugins
        self.results = []


    def connect(self, namespace="root\\cimv2"):
        from pysamba.twisted.reactor import eventContext
        log.debug("connect to %s, user %r", self.host, self.user)
        if not self.user:
            log.warning("Windows login name is unset: "
                        "please specify zWinUser and "
                        "zWinPassword zProperties before adding devices.")
            raise BadCredentials("Username is empty")
        self._wmipool[namespace] = Query()
        creds = '%s%%%s' % (str(self.user), str(self.passwd))
        return self._wmipool[namespace].connect(eventContext, str(self.device.manageIp),
                                                str(self.host), creds, namespace)


    def close(self, namespace=None):
        if not namespace:
            namespaces = self._wmipool.keys()
        else:
            namespaces = [namespace]
        for namespace in namespaces:
            self._wmipool[namespace].close()
            del self._wmipool[namespace]


    def parseError(self, err, query, instMap):
        err = Failure(err)
        err.value = 'Received %s from query: %s'%(err.value, query)
        log.error(err.getErrorMessage())
        results = {}
        for instances in instMap.values():
            for tables in instances.values():
                for table, props in tables:
                    results[table] = [err,]
        return results


    def parseResults(self, instances, instMap):
        results = {}
        for insts in instMap.values():
            for tables in insts.values():
                for table, props in tables:
                    results[table] = []
        for instance in instances:
            for kbKey, kbVal in instMap.iteritems():
                kbIns = []
                if kbKey != ():
                    for k in kbKey:
                        val = getattr(instance, k.lower(), None)
                        if type(val) in [str, unicode]:
                            kbIns.append('"%s"'%val)
                        else:
                            kbIns.append(str(val))
                    if tuple(kbIns) not in kbVal: continue
                for table, properties in kbVal[tuple(kbIns)]:
                    result = {}
                    if len(properties) == 0:
                        properties = instance.__dict__.keys()
                    if type(properties) is not dict:
                        properties = dict(zip(properties, properties))
                    for name, anames in properties.iteritems():
                        if name is '_class_name': continue
                        res = getattr(instance, name.lower(), None)
                        if type(res) is str:
                            r = DTPAT.search(res)
                            if r:
                                g = r.groups()
                                if g[8] == '000':
                                    tz = 'GMT'
                                else:
                                    hr, mn = divmod(int(g[8]), 60)
                                    if 0 < mn < 1: mn = mn * 60
                                    tz = 'GMT%s%02d%02d' % (g[7], hr, mn)
                                res = DateTime(int(g[0]), int(g[1]), int(g[2]),
                                                int(g[3]),int(g[4]),
                                                float('%s.%s'%(g[5],g[6])), tz)
                        if type(anames) is not tuple: anames = (anames,)
                        for aname in anames: result[aname] = res
                    results[table].append(result)
        return results


    def query(self, queries, includeQualifiers=True):
        instMap = {}
        for table, query in queries.iteritems():
            instMap = sortQuery(instMap, table, query)
        return self.sortedQuery(instMap, includeQualifiers=includeQualifiers)


    def sortedQuery(self, queries, includeQualifiers=False):
        def inner(driver):
            try:
                queryResult = {}
                for namespace, classes in queries.iteritems():
                    namespace=str(namespace)
                    yield self.connect(namespace=namespace)
                    try:
                        driver.next()
                    except WMIFailure, ex:
                        raise Exception("Connection error %s"%str(ex))
                    for classname, instMap in classes.iteritems():
                        plst = set()
                        for keyprops, insts in instMap.iteritems():
                            for tables in insts.values():
                                for (table, props) in tables:
                                    if props == {}:
                                        plst = ['*']
                                        break
                                    plst = plst.union(props.keys())
                                if plst == ['*']: break
                            if plst == ['*']: break
                            plst = plst.union(keyprops)
                        if includeQualifiers: plst = ['*']
                        classname=str(classname)
                        if classname.upper().startswith('SELECT '):
                            query = classname
                        elif () in instMap or len(instMap) > 1 or \
                                                len(instMap.values()[0]) > 1:
                            query="SELECT %s FROM %s"%(','.join(plst),classname)
                        else:
                            kb = zip(instMap.keys()[0],
                                    instMap.values()[0].keys()[0])
                            query="SELECT %s FROM %s WHERE %s"%(','.join(plst),
                                    classname,
                                    " AND ".join(['%s=%s'%v for v in kb]))
                        query = query.replace ("\\", "\\\\") 
                        log.debug("Query: %s", query)
                        yield self._wmipool[namespace].query(query)
                        result = driver.next()
                        instances = []
                        while 1:
                            more = None
                            yield result.fetchSome(includeQualifiers=includeQualifiers)
                            try:
                                more = driver.next()
                            except WMIFailure, ex:
                                queryResult.update(self.parseError(ex, query,
                                                                    instMap))
                                break
                            if not more:
                                queryResult.update(self.parseResults(instances,
                                                                    instMap))
                                break
                            instances.extend(more)
                    self.close(namespace=namespace)
                yield defer.succeed(queryResult)
                driver.next()
            except Exception, ex:
                log.debug("Exception collecting query: %s", str(ex))
                self.close()
                raise
        return drive(inner)

    def run(self):
        def inner(driver):
            try:
                for plugin in self.plugins:
                    pluginName = plugin.name()
                    log.debug("Sending queries for plugin: %s", pluginName)
                    log.debug("Queries: %s" % str(plugin.queries(self.device)))
                    try:
                        yield self.query(plugin.queries(self.device),
                                                    plugin.includeQualifiers)
                        self.results.append((plugin, driver.next()))
                    except Exception, ex:
                        self.results.append((plugin, ex))
            except Exception, ex:
                raise
        d = drive(inner)
        def finish(result):
            if self.datacollector:
                self.datacollector.clientFinished(self)
            else:
                reactor.stop()
        d.addBoth(finish)
        return d


    def getResults(self):
        """
        返回结果
        """
        return self.results
