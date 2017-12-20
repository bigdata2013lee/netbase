#coding=utf-8
from products.netReport.baseReport import BaseReport
class DiskReport(BaseReport):
    """
        磁盘报表
    """        
    def topTenFileSystem(self):
        """
                磁盘利用率Top10
        """
        fileSystemResult=[]
        for monitorObj in self.monitorObjs:
            if not hasattr(monitorObj,"fileSystems"):continue
            for fsys in monitorObj.fileSystems:
                title=monitorObj.titleOrUid()
                objFsys={"title":title}
                objFsys["capacity"]=self.setPower(fsys.capacity)
                blockSize=fsys.blockSize
                usedCapacity=self.prd.diskUsedCapacity(fsys,blockSize)
                utilization=self.prd.diskUtilization(fsys,usedCapacity)
                objFsys["usedCapacity"]=self.setPower(usedCapacity)
                objFsys["utilization"]=utilization
                objFsys["uname"]=fsys.uname
                fileSystemResult.append(objFsys)
        topTenFSys=sorted(fileSystemResult,
                         key=lambda x:x["utilization"],reverse=True)[:10]
        return topTenFSys
    
    def setPower(self,number):
        """
                单位转换
        """
        if not number:return number
        powers = ("k","M","G")
        if number < 1000: return "%.2f" % (number)
        for power in powers:
            number = number / 1000.0
            if number < 1000:
                return "%0.2f%s" % (number,power)
        return "%.2f%s" % (number,powers[-1])

    def getReport(self):
        """
                磁盘报表
        """
        return self.topTenFileSystem()
        