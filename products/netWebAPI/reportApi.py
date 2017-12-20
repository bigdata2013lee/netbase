#coding=utf-8
from products.netWebAPI.base import BaseApi, apiAccessSettings
from products.netPublicModel.userControl import UserControl
from products.netReport.reportRule import ReportRule
from products.netReport.reportBuild import ReportBuild
from products.netUtils import jsonUtils
from products.netReport.exportReport import ExportReport

class ReportApi(BaseApi):
    
    def getAllReportRules(self):
        """
                得到用户的所有报表配置
        """
        conditions={}
        UserControl.addCtrlCondition(conditions)
        rpt = ReportRule._findObjects(conditions=conditions)
        rs = jsonUtils.jsonDocList(rpt)
        return rs
    
    def getReport(self,uid):
        """
                得到报表
        """
        rpt = ReportRule._loadObj(uid)
        rbd=ReportBuild(rpt)
        rs=rbd.getBuildedReport()
        return rs
    
    def exportReport(self,etype="pdf",htmlContent=""):
        """
                报表导出
        """
        user = UserControl.getUser()
        if user.isExpired():
            return {False:"auth_warn:帐号已过期或欠费，无法进行相关操作，请及时充值..."}
        ert=ExportReport(user.getUid())
        toPath=ert.exportReport(etype,htmlContent)
        if toPath is None:return {False:"导出报表失败!"} 
        return {True:toPath}
    
    def getReportRule(self,uid):
        """
                得到报表配置规则
        """
        rpt = ReportRule._loadObj(uid)
        return jsonUtils.jsonDoc(rpt)
    
    @apiAccessSettings("add")
    def addReportRule(self,medata):
        """
                添加报表配置规则
        """
        user = UserControl.getUser()
        ownCompany = user.ownCompany 
        rpt =ReportRule()
        rpt.__extMedata__(medata)
        rpt.ownCompany=ownCompany
        rpt._saveObj()
        return "成功新增一个报表配置！"
    
    @apiAccessSettings("edit")
    def editReport(self,uid,medata):
        """
                编辑报表
        """
        rpt = ReportRule._loadObj(uid)
        if not rpt: return "warn:操作失败"
        rpt.__extMedata__(medata)
        rpt._saveObj()
        return "成功更新一个报表配置！"
    
    @apiAccessSettings("del")
    def delReport(self,uid):
        """
                删除报表
        """
        rpt = ReportRule._loadObj(uid)
        if not rpt: return "warn:操作失败"
        rpt.remove()
        return "成功删除一个报表配置！"    