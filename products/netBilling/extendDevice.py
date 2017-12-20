#coding=utf-8
from products.netModel.centerDocModel import CenterDocModel
from products.netModel import medata


class ExtendDevice(CenterDocModel):

    dbCollection = 'ExtendDevice'
    
    def __init__(self, uid=None):
        CenterDocModel.__init__(self)
        self.__extMedata__(dict( _id=uid))
        
    
    deviceCount = medata.plain("deviceCount",0)
    websiteCount = medata.plain("websiteCount",0)
    networkCount = medata.plain("networkCount",0)
    status = medata.plain("status",0)
    money = medata.plain("money",0.0)
    user = medata.doc("user")
    
    
if __name__ == "__main__":
    pass