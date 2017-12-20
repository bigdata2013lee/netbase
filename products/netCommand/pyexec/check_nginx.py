#coding=utf-8
from optparse import OptionParser
import sys
import urllib2
import re 
import commands
class NginxStatsPlugin:
    def __init__(self, host, port,useSsl, url, username,password):
        self.host = host
        self.port = port
        self.useSsl = useSsl
        self.url = url
        self.username=username
        self.password=password

    def run(self):
        metrics ={}
       
        if self.useSsl:
            top_url="https://%s:%s%s?XML=true" % (self.host,self.port,self.url)
        else: 
            top_url="http://%s:%s%s?XML=true" % (self.host,self.port,self.url)
          
        if self.username or self.password:
            password_mgr=urllib2.HTTPPasswordMgrWithDefaultRealm()
            password_mgr.add_password(None,top_url,self.username,self.password)
            hander=urllib2.HTTPBasicAuthHandler(password_mgr)
            opener =urllib2.build_opener(hander)
            urllib2.install_opener(opener)
            
        try:               
            response = urllib2.urlopen(top_url)            
            if response==None:
                print response.reason
                sys.exit(1)
            data = response.read()
            patt = re.compile('[0-9]+')
            m = re.findall(patt,data)
            metrics["connection"]=m[0]
            metrics["reqPerSec"]=float(m[3])*60
            metrics["errorPerSec"]=float(int(m[1])-int(m[2]))*60
            
        except SystemExit:
            sys.exit(1)
        except Exception, e:
            print str(e)
            sys.exit(1)
            
        p = re.compile(r"Server:(.+)\r")
        command ="curl -I http://%s:%s" %(self.host,self.port)
        s=commands.getoutput(command).replace(' ','')
        metrics["mwVersion"]=re.findall(p,s)[0].replace(' ','')

        if not metrics:
            print "no metrics were returned"
            sys.exit(1)
        print "STATUS OK|%s" % (' '.join([ "%s=%s" % (m[0],m[1]) \
            for m in metrics.items() ]))
if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option('-H', '--host', dest='host',
        default="192.168.2.234",
        help='Hostname of nginx server')
    parser.add_option('-p', '--port', dest='port',
        type='int', default=80,
        help='Port of nginx server')
    parser.add_option('-s', '--useSsl', dest='useSsl',
        action='store_true', default=False,
        help='Use HTTPS for the connection')
    parser.add_option('-u', '--url', dest='url',
        default='/nginx-status',
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
    cmd = NginxStatsPlugin(options.host, options.port, options.useSsl, options.url,
                            options.username,options.password)
    cmd.run()
