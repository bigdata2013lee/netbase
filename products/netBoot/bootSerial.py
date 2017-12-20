#coding=utf-8
import struct
import serial
class BootSerial(object):
    """
    开机串口类
    """
    def toBytes(self,Modbus):
        """
        转化为字节流
        """
        ModbusBytes=""
        while Modbus:
            ModbusBytes+=struct.pack('B',int(Modbus[0:4],16))
            Modbus=Modbus[4:]
        return ModbusBytes
    
    def bulidSerialConn(self):
        """
        构建串口连接
        """
        serialObj = serial.Serial('com1',9600)
        serialObj.timeout = 2
        if not serialObj.isOpen():
            serialObj.open()
        return serialObj
    
    def sendCmd(self,cmd):
        """
        发送字节流控制命令
        """
        serial=self.bulidSerialConn()
        n=serial.write(cmd)
        reply16 = serial.read(n)
        reply=""
        for i in reply16:
            reply+="0x%02x"%ord(i)
        return reply

    def offPower(self,linePosition,slaveNum='01'):
        """
        关闭电源
        """
        offModbus={0:"0x050x000x000x000x000xCD0xCA",
         1:"0x050x000x010x000x000x9C0x0A",
         2:"0x050x000x020x000x000x6C0x0A",
         3:"0x050x000x030x000x000x3D0xCA",
         4:"0x050x000x040x000x000x8C0x0B",
         5:"0x050x000x050x000x000xDD0xCB",
         6:"0x050x000x060x000x000x2D0xCB",
         7:"0x050x000x070x000x000x7C0x0B"}
        offModbus="0x%s%s"%(slaveNum,offModbus[linePosition])
        ModbusBytes=self.toBytes(offModbus)
        return self.sendCmd(ModbusBytes)
        
    def onPower(self,linePosition,slaveNum='01'):
        """
        打开电源
        @slaveNum:从机号
        """
        onModbus={0:"0x050x000x000xFF0x000x8C0x3A",
         1:"0x050x000x010xFF0x000xDD0xFA",
         2:"0x050x000x020xFF0x000x2D0xFA",
         3:"0x050x000x030xFF0x000x7C0x3A",
         4:"0x050x000x040xFF0x000xCD0xFB",
         5:"0x050x000x050xFF0x000x9C0x3B",
         6:"0x050x000x060xFF0x000x6C0x3B",
         7:"0x050x000x070xFF0x000x3D0xFB"}
        onModbus="0x%s%s"%(slaveNum,onModbus[linePosition])
        ModbusBytes=self.toBytes(onModbus)
        return self.sendCmd(ModbusBytes)

    def getPowerStatus(self,linePosition,slaveNum='01'):
        """
        获取电源状态
        """
        statusModbus="0x%s0x010x000x000x000x080x3D0xCC"%slaveNum
        ModbusBytes=self.toBytes(statusModbus)
        statusAccept=self.sendCmd(ModbusBytes)
        if not len(statusAccept)>=16:return "unknown"
        powerStatus=bin(int(statusAccept[12:16], 16))[2:]
        if linePosition>=len(powerStatus):
            return "down"
        else:
            if int(powerStatus[::-1][linePosition])==0:
                return "down"
        return "up"

if __name__=="__main__":
    import time
    bs=BootSerial()
    for i in xrange(8):
        time.sleep(2)
        
    
