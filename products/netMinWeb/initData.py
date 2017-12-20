'''
Created on 2014-12-10

@author: Administrator
'''
from products.netModel.user.user import User
from products.netModel.operation.operationer import Operationer
from products.netModel.baseModel import RefDocObject
from products.netModel.device import Device
from products.netModel.website import Website
from products.netModel.network import Network
from products.netBilling.levelPolicy import LevelPolicy
from products.netModel.operation.deviceDtail import DeviceDtail
from products.netModel.user.engineerUser import EngineerUser

class InitData():
    def initData(self):
        users=User._findObjects()
        operationers=Operationer._findObjects()
        engs=EngineerUser._findObjects()
        
        for user in users:
            try:
                user.levelPolicy.getUid()
            except:
                ownCompany=user.ownCompany
                conditions={"ownCompany":RefDocObject.getRefInfo(ownCompany)}
                host = Device._countObjects(conditions)
                website = Website._countObjects(conditions)
                network = Network._countObjects(conditions)
                lp=LevelPolicy()
                if host>5:lp.deviceCount=host
                if network>5:lp.networkCount=network
                if website>5:lp.websiteCount=website
                lp._saveObj()
                user.levelPolicy=lp
                print "user %s add levelPolicy sucessfull" % user.username
                
        for operationer in operationers:
            try:
                operationer.levelPolicy.getUid()
            except:
                levelPolicy=LevelPolicy()
                levelPolicy._saveObj()
                operationer.levelPolicy=levelPolicy
                print "operationer %s add levelPolicy sucessfull" % operationer.username 
            try:
                operationer.deviceDtail.getUid()
            except:
                deviceDtail = DeviceDtail()
                deviceDtail._saveObj()
                operationer.deviceDtail=deviceDtail         
                print "operationer %s add deviceDtail sucessfull" % operationer.username
                
        for eng in engs:
            if not eng.appraisement:
                eng.appraisement={"good":0,"common":0,"bad":0,"goodRate":0.00}
                print "engineer %s add appraisement successfull" % eng.username
            if not eng.appraisement.has_key("goodRate"):
                eng.appraisement["goodRate"]=0.00
                print "engineer %s add appraisement.goodRate sucessfull" % eng.username