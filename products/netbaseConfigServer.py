#coding=utf-8
import time
import sys
from products.rpcService.server import Server
from products.netPublicModel.modelManager import initPublicModel
from products.netPublicModel.bindNetSysEvent import bindDataRootEvents
from products.netTasks import eventExpiresTask, clearUnActiveUserTask, checkUserStatusTask
from products.netTasks import emailEventsTask
reload(sys)
sys.setdefaultencoding("utf-8")

def execTasks():
    eventExpiresTask.Task().execTask() #
    clearUnActiveUserTask.Task().execTask() #清除未激活用户
    #checkCollectorStatusTask.Task().execTask() #检测收集器状态
    checkUserStatusTask.Task().execTask() #检测用户状态
    emailEventsTask.Task().execTask() #每日事件报告
    
    
def start():
    print "Netbase Config Server Start...."
    initPublicModel()
    bindDataRootEvents()
    execTasks()
    Server.start()
        

    
if __name__ == "__main__":
    
    start()
    try:
        while True:
            time.sleep(10)
            
    except KeyboardInterrupt:
        exit()
        
    
 
    
    
    
