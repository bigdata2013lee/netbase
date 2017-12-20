#coding=utf-8
import re
import time
from products.netUtils import xutils
from products.netWebAPI.base import BaseApi
from products.netCommunity.share import Share
from products.netCommunity.question import Question
from products.netModel.feedBackInfo import FeedBackInfo
from products.netPublicModel.userControl import UserControl
from products.netCommunity.shareComment import ShareComment
from products.netCommunity.questionComment import QuestionComment


class TopicApi(BaseApi):
    @classmethod
    def createQuestion(self,title="",content="",area={"d0":"","d1":""},fields=[],award={}):
        """
        创建求助
        @param title:求助的标题
        @param content:求助的内容
        @param area: 求助人所在地域，格式：area={"d0":"一级地域","d1":"二级地域"}
        @param fields: 该求助的所属的领域，格式：fields=["fields1","fields2"...,"fieldsn"]
        @param award: 该求助的悬赏信息，格式：award={"aType":money|score,"value":xxx, "status":False}
        @return 发布提示消息 
        """
        publisher=UserControl.getUser()
        if not publisher:
            return "warn:发布求助失败" 
        if not title:
            return "warn:亲，请输入标题"
        if len(title)>40:return "warn:标题最多40个字符，一个汉字算2个字符"
        if not content:
            return "warn:亲，请输入内容"
        if len(content)>2000:return "warn:内容最多2000个字符，一个汉字算2个字符"
        if not fields:
            return "warn:亲，请选择问题的领域"
        if not area["d0"]:
            return "warn:亲，请选择省份"
        if not area["d1"]:
            return "warn:亲，请选择城市"
        if award["aType"] not in ["不悬赏","人民币","积分"]:return "warn:亲，悬赏方式只能为不悬赏、人民币、积分三种"
        if award["aType"] !="不悬赏":
            if not xutils.isValiedNum(award["value"],allowZero=False):return "warn:悬赏金额只能为正数,且不能以0开头"
        awardNum=int(publisher.awardNum)
        if award["aType"]=="积分": 
            if awardNum <= 0 or int(award["value"]) > awardNum:
                return "积分余额不足，您当前的积分为 %d"% awardNum
            else:
                publisher.awardNum=awardNum-int(award["value"])
        question=Question()
        question.title=title
        question.content=content
        question.area=area
        question.fields=fields
        question.award=award
        question.ctime=time.time()
        question.publisher=publisher
        question._saveObj()
        return "发布求助成功"
    
    @classmethod


    def createShare(self,title,content,area,fields):
        """
        创建分享
        @param title:分享的标题
        @param content:分享的内容
        @param area: 分享人所在地域，格式：area={"d0":"一级地域","d1":"二级地域"}
        @param fields: 该求助的所属的领域，格式：fields=["fields1","fields2"...,"fieldsn"]
        @return 发布提示消息 
        """
        publisher=UserControl.getUser()
        if not publisher:
            return "warn:请您先登录"
        if not title:
            return "warn:请输入标题"
        if len(title)>40:return "warn:标题最多40个字符，一个汉字算2个字符"
        if not content:
            return "warn:请输入内容"
        if len(content)>2000:return "warn:内容最多2000个字符，一个汉字算2个字符"
        if not area:
            return "warn:请输入地域"
        if not fields:
            return "warn:请输入领域" 
        share=Share()
        share.title=title
        share.content=content
        share.area=area
        share.fields=fields
        share.ctime=time.time()
        share.publisher=publisher
        share._saveObj()
        return "发布分享成功"    
    
    @classmethod
    def listQuestions(self,skip=None,limit=None,sortInfo={"ctime":-1}):
        """
        列出所有的求助，并根据排序条件进行排序
        @param skip:查询求助时跳过哪些求助，默认是None
        @param limit:查询求助时限制查询的范围，默认是None
        @param sortInfo: 对查询结果进行排序，默认按发表时间进行排序
        @return 求助列表 
        """        
        publisher=UserControl.getUser()
        conditions={"publisher":publisher._getRefInfo()}
        qList=Question._findObjects(conditions=conditions, sortInfo=sortInfo, skip=skip, limit=limit)
        if qList:return qList
        return []
    
    @classmethod
    def listShares(self,skip=None,limit=None,sortInfo={"ctime":-1}):
        """
        列出所有的分享，并根据排序条件进行排序
        @param skip:查询分享时跳过哪些求助，默认是None
        @param limit:查询分享时限制查询的范围，默认是None
        @param sortInfo: 对查询结果进行排序，默认按发表时间进行排序
        @return 分享列表 
        """         
        publisher=UserControl.getUser()
        conditions={"publisher":publisher._getRefInfo()}
        sList=Share._findObjects(conditions=conditions, sortInfo=sortInfo, skip=skip, limit=limit)
        if sList:return sList
        return []
    
    @classmethod
    def commentTopic(self,topicId,content,topicType="Question",verifyCode=""):
        """
        评论一个话题
        @param topicId:话题的id
        @param content:评论的内容
        @param topicType: 话题的类型，有求助和分享两种，默认是求助类型
        @param verifyCode: 验证码
        @return 评论的提示信息
        """              
        if topicType =="Question":
            topic = Question._loadObj(topicId)
            comment=QuestionComment()
        else:
            topic = Share._loadObj(topicId)
            comment=ShareComment()
        if not topic or not comment:
            return "warn:回复失败,请重试"
        if len(content)>2000:return "warn:内容最多2000个字符，一个汉字算2个字符"
        publisher=UserControl.getUser()
        comment.topic=topic
        comment.content=content
        comment.ctime=time.time()
        comment.publisher=publisher
        comment._saveObj()
        topic.replyNum+=1
        if not topic.publisher:return "回复成功"
        if publisher !=topic.publisher:
            newComments=topic.newComments
            newCommentTopicList=topic.publisher.newCommentTopicList
            newComments.append(comment.getUid())
            newCommentTopicList.append(comment.getUid())
            topic.newComments=newComments
            topic.publisher.newCommentTopicList=newCommentTopicList
        return "回复成功"
    
    @classmethod
    def setAcceptComment(self,questionId,commentId):
        """
        采纳一个评论
        @param questionId:求助的id
        @param commentId:评论的id
        @return 采纳结果的提示信息
        """            
        question = Question._loadObj(questionId)
        publisher=UserControl.getUser()
        comment=QuestionComment._loadObj(commentId)

        if comment.accept:
            return "warn:已经采纳"
        
        if not question or not publisher:
            return "warn:采纳失败"
        
        if question.acceptComment:
            return "warn:已经采纳一个"
        
        if  publisher != question.publisher:
            return "warn:您不是问题发布者，无权操作" 
        
        if publisher == comment.publisher:
            return "warn:您不能采纳自己的答案"
        
        comment.accept=True
        if question.award["aType"]=="积分":
            comment.publisher.awardNum+=int(question.award["value"])
        question.acceptComment=comment
        return "采纳成功 %s的积分+%s" %(comment.publisher.username,question.award["value"])
    
    @classmethod
    def approveTopicComment(self,commentId,topicType="Question"):
        """
        赞一个评论
        @param commentId:评论的id
        @param topicType:话题的类型，有求助和分享两种，默认是求助类型
        @return 赞一个评论的提示信息
        """          
        if topicType !="Question":
            comment=ShareComment._loadObj(commentId) 
        else:
            comment=QuestionComment._loadObj(commentId) 
        
        publisher=UserControl.getUser()
        if not comment or not publisher:
            return "warn:不能赞"
        approveIds=comment.approveIds
        if publisher.getUid() in approveIds:
            return "warn:您已经赞过啦"
        
        comment.approveNum+=1
        approveIds.append(publisher.getUid())
        comment.approveIds = approveIds
        return comment.approveNum
    
    @classmethod
    def setReportComment(self,commentId,topicType="Question"):
        """
        举报一个评论
        @param commentId:评论的id
        @param topicType:话题的类型，有求助和分享两种，默认是求助类型
        @return 举报一个评论的提示信息
        """           
        if topicType !="Question":
            comment=ShareComment._loadObj(commentId) 
        else:
            comment=QuestionComment._loadObj(commentId) 
        userId = UserControl.getUser().getUid()
        if not comment:
            return  "warn:评论不存在"

        if userId in (comment.reporterIds or []):
            return "warn:已经收到您的举报，我们将会快速处理，谢谢"
        
        comment.reportNum+=1
        reporterIds = comment.reporterIds or  []
        reporterIds.append(userId)
        comment.reporterIds=reporterIds
        return "成功举报此评论"
     
    @classmethod
    def _getConditons(self,text="", area={"d0":"", "d1":""},fields=[]):
        """
        设置查询条件
        @param text:查询的内容包含的文字
        @param area:查询内容所属的地域，格式：area={"d0":"一级地域","d1":"二级地域"}
        @param fields:查询内容所属的技术领域，格式：fields=["fields1","fields2"...,"fieldsn"]
        @return 查询条件
        """          
        conditions={}
        if text.strip():
            patterns=[]
            texts = text.split()
            for text in texts:
                text=text.replace("\\", "\\\\")
                patterns.append(re.compile(text,re.IGNORECASE))
            conditions.update({"title":{"$all":patterns}})
            
        if  area:
            ac={}
            if area.get("d0", ""): ac["area.d0"] = area["d0"]
            if area.get("d1", ""): ac["area.d1"] = area["d1"]
            conditions.update(ac)
        
        if fields:
            conditions.update({"fields":{"$in":fields}})
            
        return conditions
    
    @classmethod
    def searchQuestions(self,text="", area={"d0":"", "d1":""},fields=[],sortInfo=None,skip=None,limit=None):
        """
        搜索求助
        @param text:搜索的求助包含的文字
        @param area: 搜索的求助所属的地域，格式：area={"d0":"一级地域","d1":"二级地域"}
        @param fields: 搜索的求助所属的技术领域，格式：fields=["fields1","fields2"...,"fieldsn"]
        @param skip:搜索求助时跳过哪些求助，默认是None
        @param limit:搜索求助时限制查询的范围，默认是None
        @param sortInfo: 对搜索结果进行排序，默认按发表时间进行排序
        @return 搜索到的求助结果集
        """        
        conditions=self._getConditons(text=text, area=area,fields=fields)          
        qList=Question._findObjects(conditions=conditions, sortInfo=sortInfo, skip=skip, limit=limit)
        objectCount=Question._countObjects(conditions=conditions)
        return {"total":objectCount, "results": qList}
     
    @classmethod
    def searchShares(self,text="", area={"d0":"", "d1":""},fields=[],sortInfo=None,skip=None,limit=None):
        """
        搜索分享
        @param text:搜索的分享包含的文字
        @param area: 搜索的分享所属的地域，格式：area={"d0":"一级地域","d1":"二级地域"}
        @param fields: 搜索的分享所属的技术领域，格式：fields=["fields1","fields2"...,"fieldsn"]
        @param skip:搜索分享时跳过哪些求助，默认是None
        @param limit:搜索分享时限制查询的范围，默认是None
        @param sortInfo: 对搜索结果进行排序，默认按发表时间进行排序
        @return 搜索到的求助结果集
        """           
        conditions=self._getConditons(text=text, area=area,fields=fields)   
        sList=Share._findObjects(conditions=conditions, sortInfo=sortInfo, skip=skip, limit=limit)
        objectCount=Share._countObjects(conditions=conditions)
        return {"total":objectCount, "results": sList}

    @classmethod
    def getAcceptComment(self,question,commentList):
        """
        time:2014-11-20
        @author: julian
        获取已采纳的评论
        @param question:评论所属的求助
        @param commentList: 求助的评论列表
        @return 已采纳的评论
        """          
        if not question:
            return None
        if not question.acceptComment:
            return None
        for accetpComment in commentList:
            if accetpComment.accept:
                return accetpComment
        return None
    
    @classmethod
    def getNewMessageNum(self):
        """
        获取最新消息的数量
        @return 新消息的数量
        """            
        user=UserControl.getUser()
        if not user: return "noUser"
        num=len(user.newCommentTopicList)
        return num
    
    @classmethod 
    def getNewMessageQuestionList(self):
        """
        获取有新评论的求助
        @return 有新评论的求助列表
        """         
        qList=self.listQuestions()
        newCommentQList=[]
        if qList:
            for q in qList:
                if len(q.newComments) > 0: newCommentQList.append(q)
        if newCommentQList: return newCommentQList 
        return []
    
    @classmethod
    def getNewMessageShareList(self):
        """
        获取有新评论的分享
        @return 有新评论的分享列表
        """               
        sList=self.listShares()
        newCommentSList=[]
        if sList:
            for s in sList:
                if len(s.newComments) > 0: newCommentSList.append(s)
        if newCommentSList: return newCommentSList 
        return []
    
    @classmethod
    def readMessage(self,topic):
        """
        读取新评论
        @param topic:话题，有求助和分享两种
        """            
        publisher=UserControl.getUser()
        if not topic:
            return "warn:话题已经不存在"
        if not publisher:
            return "warn:此话题的发表者已不存在"
        if publisher == topic.publisher:
            if topic.newComments:
                newCommentTopicList=publisher.newCommentTopicList
                newComments=topic.newComments
                for comment in newComments:
                    if  comment in newCommentTopicList:
                        newCommentTopicList.remove(comment)
                topic.newComments=[]
                publisher.newCommentTopicList=newCommentTopicList
    
    
    @classmethod
    def showOpinon(self,title,content,publisherUsername,publisherEmail):
        '''
        反馈意见
        @param title:反馈意见的标题
        @param content:反馈意见的内容
        @return: 反馈意见是否成功  
        '''
        
        if not title:
            return "warn:请您填写标题"
        if not content:
            return "warn:请您填写内容"
        feedBackInfo=FeedBackInfo()
        feedBackInfo.feedBackUser=publisherUsername
        feedBackInfo.feedBackEmail=publisherEmail
        feedBackInfo.title=title
        feedBackInfo.feedBackContent=content
        feedBackInfo._saveObj()
        return  "反馈成功，谢谢您的反馈"    
            
            
            