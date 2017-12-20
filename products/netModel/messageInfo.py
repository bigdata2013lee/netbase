#-*- coding: utf-8 -*-

import time
from products.netModel.centerDocModel import CenterDocModel
from products.netModel import medata


def getCurrentDate():
    data=time.time()
    st=time.localtime(data)
    return time.strftime("%Y-%m-%d %H:%M:%S",st)

class MessageInfo(CenterDocModel):
    dbCollection = 'MessageInfo'
    def __init__(self):
        CenterDocModel.__init__(self)
        self._medata.update(dict(
            infoTime=getCurrentDate()           
        ))
    mUser = medata.plain("mUser", "") #收件者
    mUserID = medata.plain("mUserID", "") #收件者
    mTitle = medata.plain("mTitle", "") #标题
    mContent = medata.plain("mContent", "") #内容
    mSender = medata.plain("mSender", "") #发信者
    mSenderID = medata.plain("mSenderID", "") #发信者ID
    mSenderType = medata.plain("mSenderType", 0) #发信者类 0-普通会员  1-系统管理员
    mRead =  medata.plain("mRead", 0) #未读状态 0-未读  1-已读
    mDelete =  medata.plain("mDelete", 0)  #删除状态 0-正常  1-删除
    mType =  medata.plain("mType", 1) #信息状态 0-私信 1-系统通知 
    mFsend = medata.plain("mFsend", 0) #群发状态  0-非群发 1-群发
    mTime = medata.plain("mTime",0)
    