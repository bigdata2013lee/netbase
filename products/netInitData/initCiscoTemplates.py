#coding=utf-8

from products.netInitData.ciscoTemplates.ciscoSwitchTemplates.addCiscoSwitch_Catalyst_2900_Template import startCreateCiscoSwitch_Catalyst_2900_Template
from products.netInitData.ciscoTemplates.ciscoSwitchTemplates.addCiscoSwitch_Catalyst_3500_Template import startCreateCiscoSwitch_Catalyst_3500_Template
from products.netInitData.ciscoTemplates.ciscoSwitchTemplates.addCiscoSwitch_Catalyst_3700_Template import startCreateCiscoSwitch_Catalyst_3700_Template
from products.netInitData.ciscoTemplates.ciscoSwitchTemplates.addCiscoSwitch_Catalyst_6500_Template import startCreateCiscoSwitch_Catalyst_6500_Template
from products.netInitData.ciscoTemplates.ciscoRouterTemplates.addCiscoRouter_C2600_Template import startCreateCiscoRouter_C2600_Template
from products.netInitData.ciscoTemplates.ciscoRouterTemplates.addCiscoRouter_C3600_Template import startCreateCiscoRouter_C3600_Template
from products.netInitData.ciscoTemplates.ciscoRouterTemplates.addCiscoRouter_C3700_Template import startCreateCiscoRouter_C3700_Template
from products.netInitData.ciscoTemplates.ciscoRouterTemplates.addCiscoRouter_C1700_Template import startCreateCiscoRouter_C1700_Template
from products.netInitData.ciscoTemplates.ciscoRouterTemplates.addCiscoRouter_C7200_Template import startCreateCiscoRouter_C7200_Template
from products.netInitData.ciscoTemplates.ciscoFirewallTemplates.addCiscoFirewall_PIX_520_Template import startCreateCiscoFirewall_PIX_520_Template


def initCiscoTemplates():
    
    initSwitchTemplates()
    initRouterTemplates()
    initFirewallTemplates()

def initSwitchTemplates():
    startCreateCiscoSwitch_Catalyst_2900_Template()
    startCreateCiscoSwitch_Catalyst_3500_Template()
    startCreateCiscoSwitch_Catalyst_3700_Template()
    startCreateCiscoSwitch_Catalyst_6500_Template()

def initRouterTemplates():
    startCreateCiscoRouter_C2600_Template()
    startCreateCiscoRouter_C3600_Template()
    startCreateCiscoRouter_C3700_Template()
    startCreateCiscoRouter_C1700_Template()
    startCreateCiscoRouter_C7200_Template()

def initFirewallTemplates():
    startCreateCiscoFirewall_PIX_520_Template()


if __name__ == "__main__":
    
    initCiscoTemplates()