#coding=utf-8
from products.netModel.org.networkClass import NetworkClass

def initNetworkClass():
    NetworkClass._getDbTable().remove({})
    root = NetworkClass("networkcls", "网络")
    root._saveObj()
    
    firewall = NetworkClass("firewall","防火墙")
    firewall._saveObj()
    
    switch = NetworkClass("switch","交换机")
    switch._saveObj()
    
    router = NetworkClass("router","路由器")
    router._saveObj()
    
    
    
    
    
    root.addChild(firewall).addChild(switch).addChild(router)
    
    firewallMakers = [{"uname":"juniper", "title":"Juniper"},{"uname":"cisco", "title":"Cisco"}, {"uname":"huawei", "title":"Huawei"},
                      {"uname":"checkpoint", "title":"Checkpoint"},{"uname":"H3C","title":"H3C"}
                      ]
    for maker in firewallMakers:
        _maker = NetworkClass(maker.get("uname"),maker.get("title"))
        _maker._saveObj()
        firewall.addChild(_maker)
        
    for maker in firewallMakers:
        _maker = NetworkClass(maker.get("uname"),maker.get("title"))
        _maker._saveObj()
        switch.addChild(_maker)
        
    for maker in firewallMakers:
        _maker = NetworkClass(maker.get("uname"),maker.get("title"))
        _maker._saveObj()
        router.addChild(_maker)
    
    
    
    
if __name__ == '__main__':
    initNetworkClass()
        