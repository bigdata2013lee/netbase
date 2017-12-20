#coding=utf-8
class TaskManage(object):
    """
    任务管理类,用于注册任务模块对象
    """
    task_obj = {}
    def __init__(self,rpyc):
        self.rpyc=rpyc

    def regist(self,tasktype,taskObj):
        """
        模块对象注册方法
        """
        self.task_obj[tasktype] = taskObj

    def unregist(self,tasktype):
        """
        模块注销方法
        """
        del self.task_obj[tasktype]

    def getTaskObj(self,tasktype):
        """
        通过MID获取任务对象
        """
        return self.task_obj[tasktype]

    def startRegist(self):
        from products.nbPlugin.ipservicetask import IpServiceTask
        from products.nbPlugin.perfsnmptask import PerfSnmpTask
        from products.nbPlugin.statustask import StatusTask
        from products.nbPlugin.interfacetask import InterfaceTask
        from products.nbPlugin.filesystemtask import FileSystemTask
        self.regist('service',IpServiceTask(self.rpyc))
        self.regist('snmp',PerfSnmpTask(self.rpyc))
        self.regist('status',StatusTask(self.rpyc))
        self.regist('interface',InterfaceTask(self.rpyc))
        self.regist('filesystem',FileSystemTask(self.rpyc))
        