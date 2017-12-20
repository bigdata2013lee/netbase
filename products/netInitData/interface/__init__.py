

"""
ifPerStatus：         接口的当前工作状态。有up(1),down(2),testing(3)三种
ifInOctets：          该接口累计接收的字节数
ifOutOctets：         该接口累计发送的字节数
ifInUcastPackets：    该接口累计传递给上层协议的单目传送数据包数
ifOutUcastPackets：   该接口从上层协议接收的，需要发送的单目传送包数，包括被丢弃的数据包
ifInErrors：          该接口累计接收到的错误包数
ifOutErrors：         该接口丢弃的错误包数
ifInDiscards：        该接口先接收，后丢弃的数据包数量
ifOutDiscards：       该接口接收后丢弃的需要发送的数据包数量

DERIVE：差值
GAUGE：原值
"""