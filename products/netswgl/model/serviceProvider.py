#coding=utf-8
from products.netModel import medata
from products.netswgl.model.swglDocModel import SwglDocModel

class ServiceProvider(SwglDocModel):
    "服务商"
    
    dbCollection = 'ServiceProvider'
        
        
    def __init__(self, uid=None):
        SwglDocModel.__init__(self)
        self._medata.update(dict(
            _id=uid, 
        ))
        

    businessLicense = medata.plain("businessLicense", "") #营业执照
    comLogo= medata.plain("comLogo", "") #公司Logo urlpath
    comAddr= medata.plain("comAddr", "") #公司地址
    comUrl= medata.plain("comUrl", "") #公司网址
    comTel= medata.plain("comTel", "") #公司电话
    comEmail= medata.plain("comEmail", "") #公司邮箱
    comDesc= medata.plain("comDesc", "") #公司简述
    comKeyWords = medata.plain("comKeyWords", []) #公司关键字
    cpcAddr=medata.plain("cpcAddr", {"r0":"0", "r1":""}) #公司地址/省、市 代码
    serTypes=medata.plain("serTypes", [1]) #服务类型-多选    --  1外包服务 2硬件销售 3软件销售 4系统集成
    goodRate= medata.plain("goodRate", 0) #好评率 0-100