#coding=utf-8
import zlib
import pickle
from products.netPublicModel.baseConfigModel import ConfigServiceModel
import copy
import logging
log = logging.getLogger("collectConfig")

class CollectConfig(ConfigServiceModel):
    
    def remoteGetManageObjConfigs(self,collectorIp):
        """
                功能:远程获取一个设备收集点配置
                参数:收集器uid
                作者:lb
                时间:2013.1.30
        """
        collectConfigs ={}
        self.collectorIp=collectorIp
        manageObjs = self.findManageObjsByCollectorIp(self.collectorIp)
        for obj in manageObjs:
            try:
                if obj.getComponentType()=="Website":
                    if not obj.monitored:continue
                    self.getWebSiteConfig(obj,collectConfigs)
            except Exception,ex:
                errorMessage="获取配置出错,%s"%ex.message
                log.error(errorMessage)
                return zlib.compress(pickle.dumps((False,errorMessage)),zlib.Z_BEST_COMPRESSION)
        return zlib.compress(pickle.dumps((True,collectConfigs)),zlib.Z_BEST_COMPRESSION)

    def getCptConfig(self,obj,cfg,collectConfigs):
        """
                得到收集点配置
        """
        for collectPoint in obj.collectPoints:
            cptCfg=copy.deepcopy(cfg)
            cptUid=collectPoint.getUid()
            cptTitle=collectPoint.titleOrUid()
            cptIp=collectPoint.hostIp
            cptPort=collectPoint.port
            cptHost=(cptIp,cptPort)
            if not collectConfigs.has_key(cptHost):
                collectConfigs[cptHost]=[]
            cptCfg.update(dict(cptUid=cptUid))
            cptCfg.update(dict(cptTitle=cptTitle))
            collectConfigs[cptHost].append(cptCfg)
    
    def getWebSiteConfig(self,website,collectConfigs):
        """
                功能:远程获取一个站点的配置
                参数:收集器uid
                作者:lb
                时间:2013.1.30
        """
        for template in website.templates:
            if not template:continue
            for dsname,ds in template.findDataSources('CmdDataSource').iteritems():
                if not ds.get("monitored",True):continue
                websiteCfg=dict(cuid=self.cuid,
                    collectorIp=self.collectorIp,
                    objId=website.getUid(),
                    manageId= website.getManageId(),
                    componentType = website.getComponentType(),
                    componentId ="",
                    title=website.titleOrUid(),
                    severity = 3,
                    taskName="HttpTask",
                    templateId=template.getUid(),
                    dsname =  dsname,
                    points=ds.dataPoints.keys(),
                    command = ds.getCmd(website))
                self.getCptConfig(website, websiteCfg, collectConfigs)


    def getIpServiceConfig(self,dev,collectConfigs):
        """
                功能:远程获取一个设备的IP服务配置
                参数:收集器uid
                作者:lb
                时间:2013.1.30
        """
        for sev in dev.ipServices:
            serCfg=dict(cuid=self.cuid,
                         collectorIp=self.collectorIp,
                         objId =dev.getUid(),
                         manageId= dev.getManageId(),
                         componentType = sev.getComponentType(),
                         componentId =sev.getUid(),
                         title = sev.titleOrUid(),
                         severity = 5,
                         taskName="ServiceTask",
                         port = sev.port)
            self.getCptConfig(sev, serCfg, collectConfigs)
            
