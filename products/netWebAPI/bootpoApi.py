#coding=utf-8
import time
from products.netUtils import jsonUtils
from products.netPublicModel.userControl import UserControl
from products.netWebAPI.base import BaseApi, apiAccessSettings
from products.netPublicModel.modelManager import ModelManager as MM
from products.netModel.collector import Collector
from products.netModel.bootpo import Bootpo
from products.netBilling.billingSys import BillingSys

class BootpoApi(BaseApi):
    
    
    
    def getStatus(self,obj):
        """
                通过IPMI得到设备的电源状态
        """
        bpSev = MM.getMod("bootpoSev")
        rs=bpSev.getPowerStatus(obj)
        if rs not in ["up","down","unknown"]:
            return "unknown"
        return rs

    def listBootpoObjs(self):
        
        conditions = {}
        UserControl.addCtrlCondition(conditions)
        objs = Bootpo._findObjects(conditions=conditions)
        igPs = []
        def updict(obj):
            return {"status":self.getStatus(obj), 
                     "ipmiConfig": obj.ipmiConfig,
                     "manageIp":obj.ipmiConfig.get("netIpmiIp",""),
                    }
        return jsonUtils.jsonDocList(objs, updict=updict, ignoreProperyties= igPs)    
    
    def setBootpoPower(self, bootpoId, opName):
        """
                对设备进行 开|关|重启 操作
        @param opName: 操作名 softDown|powerUp|powerDownOp|powerResetOp
        """
        user = UserControl.getUser()
        if user.isExpired():
            return "auth_warn:帐号已过期或欠费，无法进行相关操作，请及时充值..."
        
        bpSev = MM.getMod("bootpoSev")
        bp = Bootpo._loadObj(bootpoId)
        if not bp: return "warn:操作失败，设备可能不存在"
        rs = "已经成功发送了远程操作命令!"
        ops = {
               "softDown":bpSev.sentSoftDownCmd,
               "powerUp":bpSev.sentPowerUpCmd,
               "powerDownOp":bpSev.sentPowerDownCmd,
               "powerResetOp":bpSev.sentPowerResetCmd,
        }
        rs = ops.get(opName)(bp)
        return rs
      
    def getServerTime(self):
        """
        获取服务器时间
        @return: 秒数
        """
        return int(time.time())
    
    @apiAccessSettings("add")
    def addBootpo(self, title="", ipmiConfig={}, startUpIPMI=False):
        user = UserControl.getUser()
        if user.levelPolicy.bootpoCount==0:user.levelPolicy.bootpoCount=user.levelPolicy.deviceCount+user.levelPolicy.networkCount
        if BillingSys.hasEnoughPolicyForAdd(Bootpo):
            return "warn:你的开关机项目权限不足，请购买服务后再试."
        coll = Collector.getFreeCollector(Bootpo.getComponentType()) 
        if not coll: return "warn: 编辑失败！收集器分配不到，请稍后再操作！"
        ownCompany = user.ownCompany
        if not ownCompany: return "warn:添加远程开关机对象失败！"
        bootpo = Bootpo()
        bootpo.ownCompany = ownCompany
        bootpo.title = title
        bootpo.ipmiConfig = ipmiConfig
        bootpo.startUpIPMI = startUpIPMI
        bootpo.collector = coll
        bootpo._saveObj()
        return "添加远程开关机成功！"
    
    @apiAccessSettings("edit")
    def editBootpo(self, bootpoId, title="", ipmiConfig={}, startUpIPMI=False):
        bootpo = Bootpo._loadObj(bootpoId)
        if not bootpo: return "warn: 编辑失败！对象不存在"
        bootpo.title = title
        if ipmiConfig.get("netIpmiPassword", None) is None:
            ipmiConfig["netIpmiPassword"] = bootpo.ipmiConfig["netIpmiPassword"]
        bootpo.ipmiConfig = ipmiConfig
        bootpo.startUpIPMI = startUpIPMI
        bootpo._saveObj()
        return "编辑成功！"

    @apiAccessSettings("del")
    def delBootpo(self, bootpoId):
        bootpo = Bootpo._loadObj(bootpoId)
        if not bootpo:return "warn:删除失败！对象不存在"
        bootpo.remove()
        return "删除成功！"
        
        
