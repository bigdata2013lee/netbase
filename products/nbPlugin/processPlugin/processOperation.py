#coding=utf-8
#wmic /node:192.168.1.88 /user:administrator /password:netbase process call create cmd.exe
#wmic /node:192.168.1.88 /user:administrator /password:netbase process where name="cmd.exe" delete
import wmi
class ProcessOperation(object):
    """
        进程操作类
    """
    def __init__(self,remoteIp,userName,password):
        """
                初始化方法
        """
        self.c = wmi.WMI(computer=remoteIp,user=userName,
                         password=password,namespace="root\\cimv2")

    def createProcess(self,processName):
        """
                创建进程
        """
        process_id,return_value=self.c.Win32_Process.Create(CommandLine=processName)
        if not return_value:
            try:
                if self.c.Win32_Process(ProcessId=process_id):
                    return "%s进程创建成功,PID %s"%(processName,str(process_id))
            except:
                return  "%s进程创建失败,请检查配置是否正确!"%processName

    def shutdownProcess(self,processName):
        """
                关闭进程
        """
        for process in self.c.Win32_Process():
            if process.Name.find(processName)>=0:
                process.Terminate ()
        else:
            return "成功进程关闭%s!"%processName

if __name__=="__main__":
    po=ProcessOperation("192.168.1.88","administrator","netbase")
    po.createProcess("notepad.exe")
    po.shutdownProcess("notepad.exe")