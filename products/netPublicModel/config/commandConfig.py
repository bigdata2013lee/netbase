#coding=utf-8
import zlib
import pickle
from products.netPublicModel.baseConfigModel import ConfigServiceModel
from products.netCommand.netcommand import Cmd,ManageObjConfig,DataPointConfig
import logging
log = logging.getLogger("netcommand")
class CommandConfig(ConfigServiceModel):
    """
    命令行配置类
    """
    def __init__(self):
        """
        初始化函数
        """
        self.commandAttributes={"netCommandPort":"port",
                                                "netCommandUsername":"username",
                                                "netCommandPassword":"password",
                                                "netCommandLoginTimeout":"loginTimeout",
                                                "netCommandCommandTimeout":"commandTimeout",
                                                "netKeyPath":"keyPath",
                                                "netSshConcurrentSessions":"concurrentSessions"}
        
    def getDataPointConfigs(self,ds):
        """
        功能:得到数据点配置
        """
        points = []
        for dpname,dp in ds.dataPoints.iteritems():
            dpc = DataPointConfig()                                                                                                                                                                                                                                                                           
            dpc.dpname = dpname
            dpc.dataType = dp.get("type","GUAGE")
            points.append(dpc)
        return points
        
    def getComponentCommands(self,comp,commandSet):
        """
        功能:得到组件的命令
        返回:设备配置对象
        作者:wl
        时间:2013-1-6
        """
        for template in comp.templates:
            if not template:continue
            for dsname,ds in template.findDataSources('CmdDataSource').iteritems():
                if not ds.get("monitored",True): continue
                points=self.getDataPointConfigs(ds)
                parserName = ds.get("parser", "auto")
                cmd = Cmd()
                cmd.componentType = comp.getComponentType()
                cmd.componentId = cmd.componentType!= "Device" and comp.getUid() or ""
                cmd.title=comp.titleOrUid()
                cmd.templateId=template.getUid()
                cmd.connectMode =ds.get("execType", "ssh")
                cmd.cycleTime = ds.get("execCycle")
                cmd.severity = 3
                cmd.dsname =  dsname
                cmd.parser = parserName
                cmd.command = ds.getCmd(comp)
                if points:
                    cmd.points.extend(points)
                commandSet.add(cmd)

    def getManageObjCommands(self,obj):
            """
            功能:得到单个管理对象的配置
            参数:管理对象
            返回:设备配置对象
            作者:wl
            时间:2013-1-6
            """
            cmds = set()
            self.getComponentCommands(obj,cmds)
            if obj.getComponentType()=="Device":
                for comp in self.getMonitoredComponents(obj):
                    self.getComponentCommands(comp,cmds)
            if cmds:
                moc=ManageObjConfig()
                moc.cuid=self.cuid
                moc.objId=obj.getUid()
                #对象的标识,设备是IP,站点是Url
                moc.manageId= obj.getManageId()
                for propertyName,propertyValue in self.commandAttributes.iteritems():
                    setattr(moc,propertyValue,obj.commConfig.get(propertyName,None))
                if moc is not None:moc.commands = list(cmds)
                return moc
            log.warn("设备%s没有添加命令"%obj.getManageId())
            return None
    
    def remoteGetManageObjConfigs(self,collectorIp):
        """
        功能:远程获取收集器下设备的命令行配置
        参数:收集器对象uid
        作者:wl
        时间:2013.2.26
        """
        cmdConfigs = []
        manageObjs = self.findManageObjsByCollectorIp(collectorIp)
        for obj in manageObjs:
            try:
                if obj.getComponentType()=="Bootpo":continue
                if obj.getComponentType()=="Website":continue
                if not obj.monitored:continue
                cmdinfo = self.getManageObjCommands(obj)
                if not cmdinfo:continue
                cmdConfigs.append(cmdinfo)
            except Exception,ex:
                errorMessage="获取配置出错,%s"%ex.message
                log.error(errorMessage)
                return zlib.compress(pickle.dumps((False,errorMessage)),zlib.Z_BEST_COMPRESSION)
        return zlib.compress(pickle.dumps((True,cmdConfigs)),zlib.Z_BEST_COMPRESSION)
