#coding=utf-8
from products.netModel.centerDocModel import CenterDocModel
from products.netModel import medata


class Contract(CenterDocModel):
    dbCollection = 'Contract'
    
    def __init__(self,uid=None):
        CenterDocModel.__init__(self)

    startTime = medata.plain("startTime", 0.0) #合约始起时间
    endTime = medata.plain("endTime", 0.0) #合约截止时间
    advertDays = medata.plain("advertDays", 3) #广告投放天数
    serviceCustormerNum = medata.plain("serviceCustormerNum",5) #允许服务客户数
    favoriteCustormerNum = medata.plain("favoriteCustormerNum",20) #剩余收藏客户数
    oFavoriteCustormerNum = medata.plain("oFavoriteCustormerNum",20) #允许收藏客户数
    operationer=medata.doc("operationer") #运维商

    
    isValid = medata.plain("isValid", True)#合约是否有效
    