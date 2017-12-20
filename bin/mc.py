#coding=utf-8
import commands 
import ConfigParser
import os
import sys

so={}


def _loadConf(name):
    cf=ConfigParser.ConfigParser()
    cf.read("%s/etc/%s.conf" %(os.environ["NBHOME"], name))
    so["cf"] = cf
    
    
def start(mcNames=[]):
    for name in mcNames:
            
        host = "0.0.0.0"
        port = so["cf"].get(name, "port")
        m = so["cf"].get(name, "m")
        
        memCmd = r'memcached -d -u root -m %s -l %s -p %s -P %s/%s.pid' %(m,host,port,pidDir,name)
        print  memCmd
        sop = commands.getstatusoutput(memCmd)
        print "status:%s \n %s" %sop  
        
def stop(mcNames=[]):
    memCmd = r'killall memcached'
    print  memCmd
    
def restart():
    pass
    
def error():
    print "Don not support. Please enter ./mc.sh {start|stop|restart}"
        
    
    
if  __name__ == "__main__":
    
    if len(sys.argv) <= 1:
        error()
        sys.exit(0)
            
    _loadConf("memcache")
    
    allCmds = ["restart","stop","start"]
    mcNames=["session","objects","perfs"]
    
    cmd = sys.argv[1]
    if cmd not in allCmds:
        error()
        sys.exit(0)
    
    pidDir = so["cf"].get("global", "pid_dir")
    
    
    if cmd == "start":
        start(mcNames)
    elif cmd == "stop":
        stop(mcNames)
    elif cmd == "restart":
        stop(mcNames)
        start(mcNames)
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
    
        

