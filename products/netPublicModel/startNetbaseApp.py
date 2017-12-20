#coding=utf-8
import time
from products.netPublicModel.bindNetSysEvent import bindDataRootEvents
allowStartApp = True
state = False







def startApp(rpyc=True,  eventExpires=True, billing=True):
    if not allowStartApp: return
    global state
    if state: return
    state = True

    
    from products.netPublicModel.modelManager import initPublicModel
    initPublicModel()
    bindDataRootEvents()

    
    
if __name__ == "__main__":
    startApp()
    try:
        while True:
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        exit()
    
    
 
    
    
    
