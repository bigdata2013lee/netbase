#coding=utf-8
import time
from products.netWebAPI.base import BaseApi, apiAccessSettings
from products.netPublicModel.userControl import UserControl
from products.netModel.shortcutCmd import ShortcutCmd
from products.netModel.device import Device
from products.netModel.baseModel import RefDocObject
from products.netPublicModel.collectorClient import ColloectorCallClient
from products.netUtils import jsonUtils

class ShortcutCmdApi(BaseApi):
    
    @apiAccessSettings("add")
    def createCmd(self, cmd, targetDevRef, title=None, billingUid=None):
#        if BillingSys.hasEnoughPolicyForAdd(ShortcutCmd):
#            return "warn:你的命令项目权限不足，请购买服务后再试."
        
        user = UserControl.getUser()
        ownCompany = user.ownCompany

        dev = RefDocObject.getInstance(targetDevRef)
        if not dev: return "warn:创建命令失败，关联设备可能已经不存在"
        
        scc = ShortcutCmd()
        scc.ownCompany = ownCompany
        scc.cmd = cmd
        scc.targetDev = dev
        scc.title = title
        scc._saveObj()
        return "成功创建快捷命令"
    
    @apiAccessSettings("del")
    def removeCmd(self, uids):
        for uid in uids:
            scc = ShortcutCmd._loadObj(uid)
            scc.remove()
        return "删除命令成功"
    
    
    @apiAccessSettings("edit")
    def editCmd(self, cmdUid, cmd, targetDevRef, title=None):
        scc = ShortcutCmd._loadObj(cmdUid)
        if not scc: return "warn:编辑命令失败，命令可能已经不存在"
        dev = RefDocObject.getInstance(targetDevRef)
        if not dev: return "warn:编辑命令失败，关联设备可能已经不存在"
        
        scc.cmd = cmd
        scc.targetDev = dev
        scc.title = title
        
        return "编辑命令成功"
    
    def listTargetDevs(self):
        """
        列出可选的目标设备
        @note: 不支持windows 设备
        @return: [{"ip":"", "title":""},...]
        """
        rs = []
        conditions={}
        UserControl.addCtrlCondition(conditions)
        devs = Device._findObjects(conditions)
        for dev in devs:
            if not dev.isWindowsDev: #不支持windows设备
                rs.append({"ip": dev.manageIp, "title":dev.titleOrUid(), "devRef":dev._getRefInfo()})
        
        return rs
    
    def listCmds(self):
        conditions={}
        UserControl.addCtrlCondition(conditions)
        cmds = ShortcutCmd._findObjects(conditions=conditions)
        
        def updict(doc):
            dev = doc.targetDev
            if not dev: return {"targetDev": {"ref":None, "manageIp":None, "title":None}}
            return {"targetDev": {"ref":dev._getRefInfo(), "manageIp":dev.manageIp, "title":dev.titleOrUid()}}
        
        rs = jsonUtils.jsonDocList(cmds, updict=updict)
        return rs
        
    def executeCmd(self, uid):
        """
        执行命令
        @param uid: 命令UID
        """
        
        scc = ShortcutCmd._loadObj(uid)
        if not scc: return "warn:执行命令失败，命令可能已经不存在"
        if not scc.cmd: return "warn:执行命令失败，命令内容为空"
        dev = scc.targetDev
        if not dev: "warn:执行命令失败，关联设备可能已经不存在"
        ccClient = ColloectorCallClient(dev.collector.host)
        vars = {"cmd":scc.cmd, "uid":dev.getUid(),"componentType":dev.getComponentType()}
        rs = ccClient.call(ShortcutCmd.__name__, vars =vars).get("data",{})
        scc.lastExecuteTime = time.time()
        errMsg=rs.get("message","")
        if errMsg : return errMsg
        return rs.get("data",None)


    
        
        
        
        
    