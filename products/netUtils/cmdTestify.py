import commands
from products.netUtils.xutils import nbPath as _p
class CmdTestify(object):
    """
        命令行验证类
        主要用于验证snmp,wmi或者ipmi是否配置
    """
    
    @staticmethod
    def snmpTestify(obj):
        """
        snmp验证方法
        """
        try:
            commands.getoutput("snmpwalk -v 2c -c %s %s 1.3.6.1.2.1"%(obj.snmpConfig.get("netSnmpCommunity"),obj.manageIp))
            return "SNMP已配置!"
        except:
            return "该设备没有添加snmp的相关配置,请检查!"
        
    @staticmethod
    def wmiTestify(obj):
        """
        wmi验证方法
        """
        try:
            commands.getoutput("exec %s/libexec/wmic -U %s%%%s //%s 'select * from Win32_ComputerSystem'"%(_p(),
                                                    obj.wmiConfig.get("netWinUser"),obj.wmiConfig.get("netWinPassword"),obj.manageIp))
            return "wmi已配置!"
        except:
            return "该设备没有添加wmi相关配置,请检查!"
        
    @staticmethod
    def ipmiTestify(obj):
        """
        ipmi验证方法
        """
        try:
            commands.getoutput("exec %s/libexec/ipmitool -I lan -H %s -U %s -P '%s' power status "%(_p(),
                                                    obj.ip,obj.username,obj.password))
            return "ipmi已配置!" 
        except:
            return "该设备没有添加ipmi相关配置,请检查!"
        
    