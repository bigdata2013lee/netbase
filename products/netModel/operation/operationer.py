#coding=utf-8
from products.netModel import medata
from products.netModel.user.baseUser import BaseUser
from products.netModel.user.engineerUser import EngineerUser
from products.netModel.operation.operationServiceCustomer import OperationServiceCustomer

class Operationer(BaseUser):
    dbCollection = 'Operationer'
    
    def __init__(self,uid=None):
        BaseUser.__init__(self, uid)

    levelPolicy = medata.doc("levelPolicy")
    deviceDtail = medata.doc("deviceDtail")
    levelPolicyEndTime = medata.plain("levelPolicyEndTime", 9000000000000) #后面接十二个零，可以代表时间代表无穷大
   
    baseInfo = medata.plain("baseInfo",{
            "companyName":"" , #公司名称
            "bussinessLicenseNum":"", #营业执照编号
            "phoneNum":"", #联系电话
            "address":"" #公司地址           
    })
    serviceInfo = medata.plain("serviceInfo",{
            "technologyFileds":[], #技术领域
            "technologyForte":"", #技术特长
            "serviceAreas":[] #服务地域
     })
    
    companydescription = medata.plain("companydescription","")
    
    
    @property
    def engineers (self):
        return self._getRefMeObjects("operationer", EngineerUser)

    
    @property
    def serviceCustomers(self):
        """
        服务客户列表
        """ 
        return self._getRefMeObjects("operationer", OperationServiceCustomer)
        
    
    
        
