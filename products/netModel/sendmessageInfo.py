#-*- coding: utf-8 -*-

import time
from products.netModel.centerDocModel import CenterDocModel
from products.netModel import medata


def getCurrentDate():
    data=time.time()
    st=time.localtime(data)
    return time.strftime("%Y-%m-%d %H:%M:%S",st)

class SendMessageInfo(CenterDocModel):
    dbCollection = 'SendMessageInfo'
    def __init__(self):
        CenterDocModel.__init__(self)
        self._medata.update(dict(
            infoTime=getCurrentDate()           
        ))
    mUserType = medata.plain("mUserType", "") #收件人类型   0-其他账号 1-全部账号 2-普通用户 3-付费用户
    mUser = medata.plain("mUser", "") #收件者列表
    mUserID = medata.plain("mUserID", "") #收件者列表ID
    mTitle = medata.plain("mTitle", "") #标题
    mContent = medata.plain("mContent", "") #内容
    mSender = medata.plain("mSender", "") #发信者
    mSenderID = medata.plain("mSenderID", "") #发信者ID
    mRead =  medata.plain("mRead", 0) #发送状态 0-未发送  1-已发送
    mDelete =  medata.plain("mDelete", 0)  #删除状态 0-正常  1-删除
    mTime = medata.plain("mTime",0)
    