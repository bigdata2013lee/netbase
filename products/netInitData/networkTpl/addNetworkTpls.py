#coding=utf-8

from products.netInitData.networkTpl import checkpointR70
from products.netInitData.networkTpl import CiscoSwitch
from products.netInitData.networkTpl import F5BigIP
from products.netInitData.networkTpl import H3C
from products.netInitData.networkTpl import H3Chuahei
from products.netInitData.networkTpl import H3CNE40NE80
from products.netInitData.networkTpl import HILLSTONE
from products.netInitData.networkTpl import HuaWeiARRouter
from products.netInitData.networkTpl import HuaWeiEudemonFirewall
from products.netInitData.networkTpl import JuniperNetScreen
from products.netInitData.networkTpl import MCAFEE
from products.netInitData.networkTpl import redware
from products.netInitData.networkTpl import ruijie
from products.netInitData.networkTpl import TopSec32100
from products.netInitData.networkTpl import TopSec32884
from products.netInitData.networkTpl import zte10

def createNetworkTpls():
    checkpointR70.createCheckpointR70Tpl()
    CiscoSwitch.createCiscoSwitchTpl()
    F5BigIP.createF5BigIPTpl()
    H3C.createH3CTpl()
    H3Chuahei.createH3ChuaheiTpl()
    H3CNE40NE80.createH3CNE40NE80Tpl()
    HILLSTONE.createHILLSTONETpl()
    HuaWeiARRouter.createHuaWeiARRouterTpl()
    HuaWeiEudemonFirewall.createHuaWeiEudemonFirewallTpl()
    JuniperNetScreen.createJuniperNetScreenTpl()
    MCAFEE.createMCAFEETpl()
    redware.createRedwareTpl()
    ruijie.createRuijieTpl()
    TopSec32100.createTopSec32100Tpl()
    TopSec32884.createTopSec32884Tpl()
    zte10.createZTE10Tpl()
    
if __name__=="__main__":
    createNetworkTpls()