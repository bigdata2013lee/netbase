#coding=utf-8
from optparse import OptionParser
from time import sleep
import commands
import cPickle
import re
from products.netUtils.xutils import nbPath as _p

def parse_args():
    parser = OptionParser()
    parser.add_option('-H', '--host',     dest='host',    default='211.154.143.238',help='netIpmiIp')
    parser.add_option('-u', '--username', dest='username',default='root',           help='netIpmiUserName')
    parser.add_option('-p', '--password', dest='password',default='netbase',        help='netIpmiPassword')
    parser.add_option('-s', '--Id',       dest='Id',      default='64',             help='Id')
    options, args = parser.parse_args()
    return options

def saveData(filename,data=""):
    g = open(filename,"w")
    cPickle.dump(data,g)
    g.close()

def getData(filename):
    f = open(filename)
    data = cPickle.load(f)
    f.close()
    return data

def anlyData(ipmidata="",Id=0):
    patt = re.compile("(%s: .+?)\n" %Id)

    for line in re.findall(patt,ipmidata):
        print line

if __name__ == "__main__":
    options = parse_args()
    command = _p("/libexec/ipmi-sensors -h %s -u %s -p %s" %(options.host,options.username,options.password))

    Id = options.Id
    filename = _p("/products/netCommand/pyexec/%s" %options.host)
    output = commands.getoutput(command)
    if output.find("password verification timeout") > 0:
        #sleep(4)
        data = getData(filename)
        anlyData(data,Id)
    else:
        saveData(filename,output)
        anlyData(output,Id)
        
        
        