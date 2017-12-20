#coding=utf-8
###########################################################################
#       
#
#此软件版权为深圳商之杰科技有限公司所有,更多信息请访问www.netbase.asia
#
#
###########################################################################

__doc__ = """
磁盘组件配置获取
"""
from products.dataCollector.plugins.CollectorPlugin \
    import SnmpPlugin,GetTableMap

class HRFileSystemMap(SnmpPlugin):

    maptype = "FileSystemMap"
    compname = "os"
    relname = "filesystems"
    modname = "products.netModel.filesystem"
    deviceProperties = SnmpPlugin.deviceProperties + (
      'zFileSystemMapIgnoreNames','zFileSystemMapIgnoreTypes')

    columns = {
         '.1': 'snmpIndex',
         '.2': 'type',
         '.3': 'uname',
         '.4': 'blockSize',
         '.5': 'totalBlocks',
         }

    snmpGetTableMaps = (
        GetTableMap('fsTableOid','.1.3.6.1.2.1.25.2.3.1',columns),
    )

    typemap = {
        ".1.3.6.1.2.1.25.2.1.1": "other",
        ".1.3.6.1.2.1.25.2.1.2": "ram",
        ".1.3.6.1.2.1.25.2.1.3": "virtualMemory",
        ".1.3.6.1.2.1.25.2.1.4": "fixedDisk",
        ".1.3.6.1.2.1.25.2.1.5": "removableDisk",
        ".1.3.6.1.2.1.25.2.1.6": "floppyDisk",
        ".1.3.6.1.2.1.25.2.1.7": "compactDisk",
        ".1.3.6.1.2.1.25.2.1.8": "ramDisk",
        ".1.3.6.1.2.1.25.2.1.9": "flashMemory",
        ".1.3.6.1.2.1.25.2.1.10": "networkDisk",
        }

    def process(self,device,results,log):
        """
        解析磁盘数据
        ＠device:设备对象
        """
        datamaps=[]
        getdata,tabledata = results
        fsTableOid = tabledata.get("fsTableOid")
        if not fsTableOid:
            errMsg="无法获取数据,请检查SNMP配置是否正确!"
            log.warn(errMsg)
            return errMsg,datamaps
        for snmpindex,value in fsTableOid.iteritems():
            totalBlocks = value.get("totalBlocks")
            if not totalBlocks:
                continue
            disktype = self.typemap.get(value.get("type"))
            if disktype != "fixedDisk":
                continue
            value["type"]=disktype
            import chardet
            uname=value.get("uname","")
            try:
                rs=chardet.detect(uname)
                value["uname"]=uname.decode(rs.get("encoding","utf-8"))
            except:pass
            datamaps.append(value)
        return "",datamaps
