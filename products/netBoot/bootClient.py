#coding:utf-8

import ssl
import socket
from products.netUtils.xutils import nbPath as _p

def getSocket(host, port=12305):

    ADDR = (host, port)
    TCPClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sslSock = ssl.wrap_socket(TCPClient,
                           ca_certs=_p("/bin/cacert.pem"),
                           cert_reqs=ssl.CERT_REQUIRED)
    sslSock.connect(ADDR) 
    return sslSock

def sendBootpoCmd(host, port, jsonVars):
    tcpClient=None
    try:  
        tcpClient = getSocket(host, port=port)
        tcpClient.send(jsonVars)
        tcpClient.settimeout(30)
        try:
            while True:
                data=tcpClient.recv(1024)
                if data:
                    break
        except:
            data="warn:开机命令超时,请检查网络连接是否正常!"
        finally:tcpClient.close()
    except socket.gaierror, e:  
        data='warn:连接服务器地址错误:%s'%e
    except socket.error, e:  
        data='warn:连接服务器出错!'
    return data


    
    
    
    

