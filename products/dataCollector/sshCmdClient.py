#coding=utf-8
import paramiko

class SshCmdClient():
    def  __init__(self, hostname, port, username, password):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.client = None
        
    def  login(self):
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.WarningPolicy())
        client.connect(self.hostname, self.port, self.username, self.password)
        self.client = client
    
    def logout(self):
        client = self.client
        client.close()
    
    def  execCmd(self, cmdStr):
        client = self.client
        stdin, stdout, stderr = client.exec_command(cmdStr)
        out = stdout.readlines()
        
        return "".join(out)
    
    
        
if  __name__ == "__main__":
    pass

    
    
    