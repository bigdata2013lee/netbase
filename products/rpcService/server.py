#coding=utf-8
import threading
from rpyc import Service
from rpyc.utils.server import ThreadedServer, ThreadPoolServer
from products.netUtils.settings import ManagerSettings
settings = ManagerSettings.getSettings()


class Server(object):
    @staticmethod
    def start(hostname="0.0.0.0", port=settings.getAsInt("rpycConnection","rpcPort")):

        def runService():
            s = ThreadedServer(NetbaseRpcService, auto_register=False,
                                    hostname=hostname, port=port,
                                    protocol_config={"allow_public_attrs" : True, 'allow_setattr':True})
            s.start()
        
        th = threading.Thread(target=runService)
        th.setDaemon(True)
        th.start()




class NetbaseRpcService(Service):

    def on_connect(self):
        # code that runs when a connection is created
        # (to init the serivce, if needed)
        print "rpyc on connect."

    def on_disconnect(self):
        # code that runs when the connection has already closed
        # (to finalize the service, if needed)
        print "rpyc on disconnect."
        
    def exposed_getDataRoot(self):
        """
        dataRoot为Rpyc提供具体服务内容
        """
        from products.netPublicModel.modelManager import ModelManager
        dr = ModelManager.getMod('dataRoot')
        return dr

    def exposed_getCSM(self, configClass):
        "获取配置转换模块对象"
        from products.netPublicModel.modelManager import ModelManager
        csm = ModelManager.getMod(configClass)
        return csm

if __name__ == "__main__":
    Server.start()














