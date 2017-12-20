#coding=utf-8

class BaseClient(object):

    def __init__(self, device, datacollector):
        """
                初始化
        """
        self.hostname = None
        if device:
            self.hostname = device.manageIp
        self.device = device
        self.datacollector = datacollector
        self.timeout = None
        self.timedOut = False

    def run(self):
        """
        启动
        """
        pass

    def stop(self):
        """
        停止
        """
        pass

    def getResults(self):
        """
        得到结果
        """
        return []

