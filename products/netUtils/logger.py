#coding=utf-8
'''
Created on 2012-12-11

@author: Administrator
'''


import logging.config
from logging.handlers import RotatingFileHandler
 
class Logging:
    
    logDir = "/opt/netbase4/log"
    __inited = False
    
    @staticmethod
    def _initLogConf():
        logging.config.fileConfig(Logging.logDir + "/logging.conf")
        Logging.__inited = True
    
    @staticmethod
    def getLogger(name="root"):
        if not Logging.__inited: Logging._initLogConf()
        inst = logging.getLogger(name)
        return inst
    
class NetRotatingFileHandler(RotatingFileHandler):
    def __init__(self, filename='default.log', mode='a', maxBytes=0, backupCount=0, encoding=None, delay=0):
        filename = Logging.logDir + "/" + filename
        
        RotatingFileHandler.__init__(self, filename=filename, mode=mode, maxBytes=maxBytes, 
                                     backupCount=backupCount, encoding=encoding, delay=delay)

if __name__ == "__main__":     
    logger = Logging.getLogger("netmodel")
    logger.debug("debug message")
    logger.info("info message")
    logger.warn("warn message")
    logger.error("error message")
    logger.critical("critical message")
    
   
    
