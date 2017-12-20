#coding=utf-8
from products.netModel.org.middlewareClass import MiddlewareClass

def initMiddlewareClass():
    #MiddlewareClass(uname, title)
    root = MiddlewareClass("middlewarecls", "中间件")
    root._saveObj()
    
    apache = MiddlewareClass("MwApache","Apache")
    apache._saveObj()
    
    tomcat = MiddlewareClass("MwTomcat","Tomcat")
    tomcat._saveObj()
    
    iis = MiddlewareClass("MwIis","IIS")
    iis._saveObj()
    

    nginx = MiddlewareClass("MwNginx","Nginx")
    nginx._saveObj()
           
           
    
    root.addChild(iis).addChild(tomcat).addChild(apache).addChild(nginx)
    
    
    
if __name__ == '__main__':
    initMiddlewareClass()
        