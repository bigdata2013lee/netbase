#coding=utf-8
from products.netCommunity.shareComment import ShareComment
from products.netModel.baseModel import DocModel
from products.netModel import medata


class Share(DocModel):
    dbCollection = 'Share'
    
    publisher=medata.doc("publisher")
    ctime = medata.plain("ctime",0)
    content = medata.plain("content","")
    replyNum = medata.plain("replyNum",0)
    area = medata.plain("area",{"d0":"", "d1":""})
    fields = medata.plain("fields",[])
    newComments = medata.plain("newComments",[])
    
    def __init__(self):
        DocModel.__init__(self)
        self.__extMedata__(dict())
        
    def  getComments(self, sortInfo={"ctime":-1}, skip=0, limit=None):
        """
        获得所有评论
        @param sortInfo:对查询结果进行排序，默认按发表时间进行排序
        @param skip:查询分享时跳过哪些求助，默认是None
        @param limit: 查询分享时限制查询的范围，默认是None
        @return 评论列表 
        """       
        comments=self._getRefMeObjects("share", ShareComment, 
                                       conditions={}, sortInfo=sortInfo, skip=skip, limit=limit)
        return comments    
