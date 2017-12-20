#coding=utf-8
from products.netWebAPI.base import BaseApi
from products.netModel.messageInfo import MessageInfo
from products.netModel import  mongodbManager as dbManager
from products.netPublicModel.userControl import UserControl
from products.netUtils import jsonUtils
import json
import time

class MessageApi(BaseApi):
    def addmessage(self):
        fbi =MessageInfo()
        user = UserControl.getUser()
        if user:
            fbi.mUser=user.username
            fbi.mUserID=user.getUid()
            fbi.mContent = "获取新信息总数和新信息列表获取新信息总数和新信息列表获取新信息总数和新信息列表获取新信息总数和新信息列表获取新信息总数和新信息列表"
            fbi.mSender = "Admin"
            fbi.mTime = time.time()
            fbi.mSenderID = "id"
            fbi.mTitle = "获取新信息总数和新信"
            fbi.mType = 1
            fbi._saveObj()



    def getnewmessage(self):
        """
                获取新信息总数和新信息列表
                暂时返回通知信息
        """
        user = UserControl.getUser()
        if user:
            conditions = {"mUserID":user.getUid(),"mRead":0,"mType":1}
            count = MessageInfo._countObjects(conditions);
            sortInfo = {"mTime":-1}
            rpt = MessageInfo._findObjects(conditions,sortInfo=sortInfo, skip=0, limit=4)
            rs = jsonUtils.jsonDocList(rpt)
            result = {"count":count,"item":rs}
            return json.dumps(result)

        error =  {"count":0,"item":null}
        return json.dumps(error)
    
    def getmessagelist(self,start,num):
        """
                获取通知信息
        """
        if not start: start = 0;
        if not num: num = 6;
        user = UserControl.getUser()
        if not user:
            return "请先登陆";
        conditions = {"mUserID":user.getUid(),"mType":1}
        sortInfo = {"mTime":-1}
        rpt = MessageInfo._findObjects(conditions,sortInfo=sortInfo, skip=start, limit=num)
        rs = jsonUtils.jsonDocList(rpt)
        return rs
    
    def delmessage(self,mid):
        """
                删除信息列表
        """
        minfo = MessageInfo._loadObj(mid)
        if not minfo: return "fail"
        minfo.remove()
        return "删除信息成功！"

    def clearmessage(self):
        """
                清空用户所有信息
        """
        db = dbManager.getNetCenterDB()
        user = UserControl.getUser()
        if not user:
            return "请先登陆";
        result = db.MessageInfo.remove({'mUserID':user.getUid()},safe=True)
        return "删除信息成功！"

    def readmessage(self,mid):
        """
                读取信息列表
        """
        minfo = MessageInfo._loadObj(mid)
        if not minfo: return "0"
        minfo.mRead = 1;
        minfo._saveObj();
        return "1！"
