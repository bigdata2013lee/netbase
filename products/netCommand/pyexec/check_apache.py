#coding=utf-8
from optparse import OptionParser
import sys
import urllib2
import re

class NetbaseApacheStatsPlugin:
    def __init__(self, host, port, useSsl, url, ngregex, ngerror,username,password):
        self.host = host
        self.port = port
        self.useSsl = useSsl
        self.url = url
        self.ngregex = ngregex
        self.ngerror = ngerror
        self.username = username
        self.password = password

    def run(self):
        metrics = {}
        if self.useSsl:
            url_auto="https://%s:%s%s" % (self.host,self.port,self.url)
        else: 
            url_auto="http://%s:%s%s" % (self.host,self.port,self.url)
        url = url_auto.replace("?auto","")
            
        request_auto=urllib2.Request(url_auto)
        request_html=urllib2.Request(url)
        
        if self.username or self.password:
            b64str=urllib2.base64.encodestring("%s:%s" % (self.username,self.password))
            request_auto.add_header('Authorization', 'Basic %s'%b64str)
            request_html.add_header('Authorization', 'Basic %s'%b64str)
        try:
            response_xml=urllib2.urlopen(request_auto)
            response_html=urllib2.urlopen(request_html)
            if response_xml==None:
                print 'connection falied'
                sys.exit(1)
                
            xml_doc = response_xml.read()        
            line_regex = re.compile(r'^([^:]+): (.+)$')
            for line in xml_doc.split("\n"):
                match = line_regex.search(line)
                if not match: continue
                name, value = match.groups()
                if name == 'Total Accesses':
                    metrics['connection'] = value
                elif name == 'ReqPerSec':
                    metrics['reqPerSec'] = float(value)*60
                elif name == 'BytesPerSec':
                    metrics['bytesPerSec'] = float(value)*60
                elif name == 'Uptime':
                    metrics['upTime'] = value
                  
            html_doc = response_html.read()
            patt = re.compile(r'<dt>Server Version:(.+)</dt>')
            metrics['mwVersion']=re.findall(patt,html_doc)[0].replace(' ','')         
                
            if self.ngregex:
                line_regex = re.compile(self.ngregex)
                msg = ""
                for line in xml_doc.split("\n"):
                    match = line_regex.search(line)
                    if not match: continue

                    for k, v in match.groupdict().items():
                        if v is None:
                            msg = self.ngerror
                        else:
                            metrics[k] = v
                if msg:
                    print msg + "|" + " ".join(["%s=%s" % (k, v) for k,v in metrics.items()])
                    sys.exit(1)

        except SystemExit:
            sys.exit(1)
        except Exception, e:
            print str(e)
            sys.exit(1)

        if not metrics:
            print "no metrics were returned"
            sys.exit(1)

        print "STATUS OK|%s" % (' '.join([ "%s=%s" % (m[0],m[1]) \
            for m in metrics.items() ]))

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option('-H', '--host', dest='host',
        help='Hostname of Apache server',
        default="192.168.2.235")
    parser.add_option('-p', '--port', dest='port',
        type='int', default=80,
        help='Port of Apache server')
    parser.add_option('-s', '--ssl', dest='useSsl',
        action='store_true', default=False,
        help='Use HTTPS for the connection')
    parser.add_option('-u', '--url', dest='url',
        default='/server-status?auto',
        help='Relative URL of server status page')
    parser.add_option('-r', '--regex', dest='ngregex',
        default='',
        help='A named group (!) regular expression')
    parser.add_option('-e', '--error', dest='ngerror',
        default='',
        help='Error message to send if one of the named groups return None')
    parser.add_option('-a','--username',dest='username',
        type='string',
        default='admin',
        help='username for server status page')
    parser.add_option('-b','--password',dest='password',
        type='string',
        default="admin",
        help='password of server status page')
    options, args = parser.parse_args()

    if not options.host:
        print "You must specify the host parameter."
        sys.exit(1)

    cmd = NetbaseApacheStatsPlugin(
        options.host, options.port, options.useSsl, options.url, options.ngregex,\
         options.ngerror,options.username,options.password)
    cmd.run()