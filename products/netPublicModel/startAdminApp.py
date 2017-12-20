#coding=utf-8
import time


allowStartApp = True
state = False
def startApp():
    if not allowStartApp: return
    global state
    if state: return
    state = True

    initPublicModel()
    
def initPublicModel():
    "intit public Model"
    from products.netPublicModel.dataRoot import DataRoot
    from products.netEvent.eventManager import EventManager
    from products.netPublicModel.modelManager import ModelManager
    
    ModelManager.regist('dataRoot', DataRoot())
    ModelManager.regist('eventManager', EventManager())    
    
if __name__ == "__main__":
    startApp()
    try:
        while True:
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        exit()
    
    
 
    
    
    
