#coding=utf-8
from products.netModel.user.baseUser import BaseUser
from products.netModel import medata
from products.netModel.user.user import User
from products.netModel.rechargeForm import RechargeForm

class AdminUser(BaseUser):
    dbCollection = 'AdminUser'
    
    def __init__(self, uid=None):
        BaseUser.__init__(self, uid=uid)
        self.__extMedata__(dict())
    
    phone=medata.plain("phone")
    email = medata.plain("email")
    originalName = medata.plain("originalName","") #超级管理员实际名称 
    