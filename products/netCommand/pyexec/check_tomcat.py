#coding=utf-8
from optparse import OptionParser
import sys
import urllib2
from xml.etree import ElementTree
import re

class TomcatStatsPlugin:
    
    metrics ={}
    
    def __init__(self, host, port,useSsl, url, username,password):
        self.host = host
        self.port = port
        self.useSsl = useSsl
        self.url = url
        self.username=username
        self.password=password

    def run(self): 
        if self.useSsl:
            url_xml="https://%s:%s%s?XML=true" % (self.host,self.port,self.url)
            url_html="https://%s:%s%" % (self.host,self.port,self.url)
        else: 
            url_xml="http://%s:%s%s?XML=true" % (self.host,self.port,self.url)
            url_html="http://%s:%s%s" % (self.host,self.port,self.url)
            
        request_xml=urllib2.Request(url_xml)
        request_html=urllib2.Request(url_html)
        
        if self.username or self.password:
            b64str=urllib2.base64.encodestring("%s:%s" % (self.username,self.password))
            request_xml.add_header('Authorization', 'Basic %s'%b64str)
            request_html.add_header('Authorization', 'Basic %s'%b64str)
        try:  
            response_xml=urllib2.urlopen(request_xml)
            response_html=urllib2.urlopen(request_html)
            if (response_xml==None)or(response_html==None):
                print 'connection falied'
                sys.exit(1)
                
            html_doc = response_html.read()
            self.analyHtml(html_doc)
  
            tree = ElementTree.parse(response_xml)
            root= tree.getroot() 
                              
            for node in root:
                if node.tag=='jvm':
                    self.analyJVM(node)                                                          
                if node.tag=='connector':
                    self.analyConnector(node) 
                    
        except SystemExit:
            sys.exit(1)
        except Exception, e:
            print str(e)
            sys.exit(1)
            
        if not self.metrics:
            print "no self.metrics were returned"
            sys.exit(1)
        print "STATUS OK|%s" % (' '.join([ "%s=%s" % (m[0],m[1]) \
            for m in self.metrics.items() ]))
            
    def analyHtml(self,html_doc):
        patt = re.compile(r'<small>(.+)</small>')
        serverInformation = re.findall(patt,html_doc)
        length = len(serverInformation)
        self.metrics['mwVersion']=serverInformation[length/2].replace(' ','')
        self.metrics['osVersion']=(serverInformation[length/2+3]+'-'+serverInformation[length/2+4]).replace(' ','')
        self.metrics['jvmVersion']=serverInformation[length/2+1].replace(' ','')


    def analyJVM(self,node):
        node_child_list=node.getchildren()
        for node_child in node_child_list:
            msg=node_child.attrib
            if node_child.tag=='memory':
                self.metrics["totalMem"] =msg["total"]
                self.metrics["freeMem"]  =msg["free"]
                    
    def analyConnector(self,node):
        node_msg=node.attrib
        pattern = re.compile(r'"?https?-.+"?')                                          
        m = re.match(pattern,node_msg['name'])
        if m:
            node_child_list=node.getchildren()
            for node_child in node_child_list:
                msg=node_child.attrib
                if node_child.tag=='threadInfo':
                    self.metrics['cThreadCount'] = msg['currentThreadCount']
                    self.metrics['cThreadsBusy'] = msg['currentThreadsBusy']                  
                if node_child.tag=='requestInfo':
                    self.metrics['reqPerSec'] = float(msg['requestCount'])*60
                    self.metrics['errorPerSec'] = float(msg['errorCount'])*60
                    self.metrics['bytesPerSec'] = float(int(msg['bytesReceived'])+int(msg['bytesSent']))*60
                                    
if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option('-H', '--host', dest='host',
        default="192.168.2.237",
        help='Hostname of Apache server')
    parser.add_option('-p', '--port', dest='port',
        type='int', default=80,
        help='Port of Apache server')
    parser.add_option('-s', '--ssl', dest='ssl',
        action='store_true', default=False,
        help='Use HTTPS for the connection')
    parser.add_option('-u', '--url', dest='url',
        default='/manager/status',
        help='Relative URL of server status page')
    parser.add_option('-a','--username',dest='username',
        type='string',
        default='admin',
        help='username for server status page')
    parser.add_option('-b','--password',dest='password',
        type='string',
        default="admin",
        help='password of server status page')

    options, args = parser.parse_args()
    cmd = TomcatStatsPlugin(options.host, options.port, options.ssl, options.url,
                            options.username,options.password)
    cmd.run()