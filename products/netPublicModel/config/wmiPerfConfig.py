#coding=utf-8
import zlib
import pickle
from products.netPublicModel.baseConfigModel import ConfigServiceModel
import logging
log = logging.getLogger("netperfwmi")
class WinDeviceConfig(object):
    """
    功能:构建一个windows设备配置类
    作者:wl
    时间:2013-2-20
    """
    device = ''
    ipAddress=''
    wmiProxy =''
    winUser = ''
    winPassword = ''
    wmiMonitorIgnore=False
    queries=''
    datapoints=''
    
    
class WmiConfig(ConfigServiceModel):
    """
    wmi配置类
    """
    def getWmiInstanceInfo(self,ds):
        """
        得到wmi实例的信息
        """
        classname = ds.get("cmd")
        namespace =str(ds.get("nameSpace").replace("\\", "/"))
        transport = ds.get("sourceType")
        if classname.upper().startswith('SELECT '):
            return (transport, classname, {}, namespace)
        kb = classname.split('.', 1)
        cn = kb[0].split(':', 1)
        if len(cn) > 1:
            classname = cn[1]
            namespace = cn[0]
        else: classname = cn[0]
        if len(kb) > 1: kb = kb[1]
        else: return (transport, classname, {}, namespace)
        keybindings = {}
        for key in kb.split(','):
            try: var, val = key.split('=', 1)
            except: continue
            keybindings[var] = val
        return (transport, classname, keybindings, namespace)

    def sortQuery(self,qs, table, query):
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

    def getWbemComponentConfig(self,transports, comp, queries, datapoints):
        """
                功能:得到组件的命令
                返回:设备配置对象
                作者:wl
                时间:2013-1-6
        """
        for template in comp.templates:
            if not template:continue
            for dsname,ds in template.findDataSources('WmiDataSource').iteritems():
                if not ds.get("monitored",True): continue
                transport, classname, kb, namespace = self.getWmiInstanceInfo(ds)
                if transport != transports[0]: continue
                qid = comp.getUid() + "_" + template.getUid() + "_" + ds.uname
                datapoints[qid] = []
                properties = {}
                for dpname,dp in ds.dataPoints.iteritems():
                    alias = dpname.strip()
                    dpType = dp.get("type","GUAGE")
                    if alias not in properties: properties[alias] = (dpname,)
                    else: properties[alias] = properties[alias] + (dpname,)
                    datapoints[qid].append((comp.getUid(),
                                        comp.titleOrUid(),
                                        comp.getComponentType(),
                                        template.getUid(),
                                        ds.uname,
                                        dpname,
                                        dpType))                                                                                                                                                                                                             
                queries = self.sortQuery(queries,qid,(classname,kb,namespace,properties))

    def getWbemDeviceConfig(self,trs, device):
        queries = {}
        datapoints = {}
        self.getWbemComponentConfig(trs, device, queries, datapoints)
        return queries, datapoints

    def getWmiConfig(self,obj):
        self.cimtransport = ['WMI', 'CIM']
        wdc=WinDeviceConfig()
        wdc.cuid=self.cuid
        wdc.objId=obj.getUid()
        wdc.manageIp=obj.manageIp
        wdc.manageId= obj.getManageId()
        wdc.wmiProxy =""
        wdc.winUser =obj.wmiConfig.get("netWinUser","administrator")
        wdc.winPassword =obj.wmiConfig.get("netWinPassword","netbase")
        wdc.queries, wdc.datapoints = self.getWbemDeviceConfig(
                                                            self.cimtransport,
                                                            obj)
        if not wdc.queries:
            return None
        return wdc

    def remoteGetManageObjConfigs(self,collectorIp):
        """
                远程获取WMI配置
        """
        wmiConfigs = []
        manageObjs = self.findManageObjsByCollectorIp(collectorIp)
        for obj in manageObjs:
            try:
                if not hasattr(obj, "wmiConfig"):continue
                if obj.wmiConfig is None:continue
                if not obj.monitored:continue
                wdc=self.getWmiConfig(obj)
                if not wdc:continue
                wmiConfigs.append(wdc)
            except Exception,ex:
                errorMessage="获取配置出错,%s"%ex.message
                log.error(errorMessage)
                return zlib.compress(pickle.dumps((False,errorMessage)),zlib.Z_BEST_COMPRESSION)
        return zlib.compress(pickle.dumps((True,wmiConfigs)),zlib.Z_BEST_COMPRESSION)
            
