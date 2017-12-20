#coding=utf-8
#--------------------华为--------------------------------------#

companys = ["huawei", "juniper", "checkpoint", "cisco", "H3C", "hillstone", "F5", "ruijie", "redware", "zte", "TopSec"]

networkDevice = {
    "/networkcls/firewall/huawei":{
        "huawei_firewall_Eudemon":["BaseTpl_HuaWeiEudemonFirewall"],
    },
    "/networkcls/switch/huawei":{

    },
    "/networkcls/router/huawei":{
        "huawei_router_ARR":["BaseTpl_HuaWeiARRouter"],
    },
#--------------------juniper--------------------------------------#             
    "/networkcls/firewall/juniper":{
        "juniper_firewall_B1":["BaseTpl_JuniperFireWall"],
        "juniper_firewall_NS5GT-ADSL":["BaseTpl_JuniperFireWall"],

    },
    "/networkcls/switch/juniper":{
  
    },
    "/networkcls/router/juniper":{
   
    },  
                 
                 
#---------------checkpoint-------------------------------------------#             
    "/networkcls/firewall/checkpoint":{
        "checkpoint_firewall_checkPoint":["BaseTpl_CheckPoint"],
        "checkpoint_firewall_checkPointR70":["BaseTpl_CheckpointR70"],
    },
    "/networkcls/switch/checkpoint":{

    },
    "/networkcls/router/checkpoint":{
 
    },
                 
    #--------------思科--------------------------------------------#             
    "/networkcls/firewall/cisco":{
        "cisco_firewall_PIX_520":["BaseTpl_CiscoFirewall_PIX_520"],
    },
    "/networkcls/switch/cisco":{
        "cisco_switch_Catalyst_2900":["BaseTpl_CiscoSwitch_Catalyst_2900"],
        "cisco_switch_Catalyst_3500":["BaseTpl_CiscoSwitch_Catalyst_3500"],
        "cisco_switch_Catalyst_6500":["BaseTpl_CiscoSwitch_Catalyst_6500"],
        "cisco_switch_Catalyst_3700":["BaseTpl_CiscoSwitch_Catalyst_3700"],
        "cisco_switch_Catalyst_2950":["BaseTpl_CiscoSwitch_Catalyst_2950"],
        "cisco_switch_Catalyst_2960":["BaseTpl_CiscoSwitch_Catalyst_2960"],
        "cisco_switch_Catalyst_2960G48":["BaseTpl_CiscoSwitch_Catalyst_2960G48"],
        "cisco_switch_Catalyst_2970":["BaseTpl_CiscoSwitch_Catalyst_2970"],
        "cisco_switch_Catalyst_3750":["BaseTpl_CiscoSwitch_Catalyst_3750"],
  
    },
    "/networkcls/router/cisco":{
        "cisco_router_C2600":["BaseTpl_CiscoRouter_C2600"],
        "cisco_router_C1700":["BaseTpl_CiscoRouter_C1700"],
        "cisco_router_C3700":["BaseTpl_CiscoRouter_C3700"],
        "cisco_router_C3600":["BaseTpl_CiscoRouter_C3600"],
        "cisco_router_C7200":["BaseTpl_CiscoRouter_C7200"],
    },
#---------------H3C-------------------------------------------#             
    "/networkcls/firewall/H3C":{

    },
    "/networkcls/switch/H3C":{
        "H3C_switch_QuidwayS2326TP-SI":["BaseTpl_H3CNE40NE80"],

    },
    "/networkcls/router/H3C":{
        "H3C_router_H3C":["BaseTpl_H3C"],
        "H3C_router_huahei":["BaseTpl_H3Chuahei"],
        "H3C_router_ne40":["BaseTpl_H3CNE40NE80"],
        "H3C_router_ne80":["BaseTpl_H3CNE40NE80"],

    },    
#---------------山石-------------------------------------------#             
    "/networkcls/firewall/hillstone":{
        "hillstone_firewall_HILLSTONE":["BaseTpl_HILLSTONE"],
    },
    "/networkcls/switch/hillstone":{

    },
    "/networkcls/router/hillstone":{

    },     
#---------------F5-------------------------------------------#             
    "/networkcls/loadBalancing/F5":{
        "F5_loadbalance_bigip":["BaseTpl_F5BigIP"],

    },
    "/networkcls/switch/F5":{

    },
    "/networkcls/router/F5":{

    },
#---------------ruijie-------------------------------------------#             
    "/networkcls/firewall/ruijie":{
        "ruijie_firewall_Ruijie":["BaseTpl_Ruijie"],

    },
    "/networkcls/switch/ruijie":{

    },
    "/networkcls/router/ruijie":{

    },
#---------------redware-------------------------------------------#             
    "/networkcls/firewall/redware":{
        "redware_loadbalance_Redware":["BaseTpl_Redware"],
 
    },
    "/networkcls/switch/redware":{
  
    },
    "/networkcls/router/redware":{
 
    },
#---------------中兴-------------------------------------------#             
    "/networkcls/firewall/zte":{
        "zte_firewall_B1":["BaseTpl_ZTE10"],

    },
    "/networkcls/switch/zte":{

    },
    "/networkcls/router/zte":{

    },
#---------------TopSec-------------------------------------------#             
    "/networkcls/firewall/TopSec":{
        "TopSec_firewall_32100":["BaseTpl_TopSec32100"],
        "TopSec_firewall_32884":["BaseTpl_TopSec32884"],
        "TopSec_firewall_X042":[],
    },
    "/networkcls/switch/TopSec":{

    },
    "/networkcls/router/TopSec":{

    },
}

#根据产品型号获取相应的根
def getRootDir(productId):
    li = productId.split("_")
    path = "/networkcls/"+li[1] + "/" + li[0]
    if networkDevice.has_key(path) and networkDevice[path].has_key(productId): 
        return path
    
    return None


def listProductIdsByGroup(group):
    """
    以某一类型作为类别，根据公司分类，列出产品型号
    """
    
    rs = []
    for company in companys:
        proKey = "/networkcls/%s/%s" %(group, company)
        proValue = networkDevice.get(proKey, {}).keys()
        if not proValue: continue
        g = dict(company=company, path=proKey, productTypes=proValue)
        rs.append(g)
    return rs
    
    
    
    
    




if __name__ == "__main__":
    
    path = getRootDir("cisco_router_C2600")
    print listProductIdsByGroup("router")
    
