#coding=utf-8
from products.netWebAPI.base import BaseApi
from products.netModel.feedBackInfo import FeedBackInfo
from products.netPublicModel.userControl import UserControl

class FeedBackInfoApi(BaseApi):
        
    def addFeedBackInfo(self,medata):
        """
                添加用户反馈信息
        """
        fbi =FeedBackInfo()
        fbi.__extMedata__(medata)
        user = UserControl.getUser()
        if user:
            feedBackUser=user.username
            fbi.feedBackUser=feedBackUser
        fbi._saveObj()
        return "成功添加反馈信息！"