#coding=utf-8
from products.netModel.baseModel import DocModel
from products.netModel import medata


class Organizer(DocModel):
    def __init__(self, uname="", title=""):
        """
                初始化函数
        @param uname: 
        @param title: 
        """
        DocModel.__init__(self)
        self._medata.update(dict(
            uname = uname, 
            title = title or uname,
        ))

    parent = medata.doc("parent")        
    ownCompany = medata.doc("ownCompany")
    
    @property
    def uname(self):
        return self._medata.get("uname")
    
    @property
    def items(self):
        """
        动态加载当前节点的子节点
        """
        return self._getRefMeObjects('parent', self.__class__)
    
    @classmethod
    def getOrganizerByUid(cls,uid):
        """
                功能:通过uid获取类对象
                参数:类对象uid
        """
        return cls._loadObj(uid)

    @classmethod
    def getRoot(cls, condition={}):
        """
        得到树形类的根节点对象
        @param cls: Organizer 子类 
        @return: cls 的根
        """
        tb = cls._getDbTable()
        _condition={"uname":cls.rootUname}
        _condition.update(condition)
        mObj = tb.find_one(_condition)
        if not mObj:return None
        root = cls._loadObjFromMap(mObj)
        return root

    
    def getPath(self):
        """"
            递归得到当前对象的路径
            @return:字符串类型的类路径
        """
        temp = {'path':''}
        def dealFun(node):
            temp['path'] = '/' + str(node.uname) + temp['path']
        
        self.traverseUp(dealFun)
        return temp['path']
    
    def getTitle(self):
        """
        得到当前对象的标题，如果标题为空，则返回对象的唯一标示
        """
        return self.title or self.uname  
        
    def getTitlePath(self):
        """
            递归得到当前节点的标题路径
            @return：字符串类型的标题路径
        """
        temp = {'path':''}
        def dealFun(node):
            title = getattr(node, 'title', None)
            if not title: title = str(node.uname) 
            temp['path'] = '/' + title + temp['path']
        
        self.traverseUp(dealFun)
        return temp['path']
        

    def getCurMonitorObjs(self, conditions={}):
        """
        子类需要实现 getCurMonitorObjs
        """
        return []
    
    def countCurMonitorObjs(self, conditions={}):
        """
        子类需要实现 countCurMonitorObjs
        """
        return 0
    
    def getAllMonitorObjs(self, conditions={}):
        """
        子类需要实现 getCurMonitorObjs
        """
        rs = []
        def dealFun(node):
            rs.extend(node.getCurMonitorObjs(conditions))
        
        self.traverseDown(dealFun)
        return rs
        
    def countAllMonitorObjs(self, conditions={}):
        rs = {"sum":0}
        def dealFun(node):
            rs["sum"]+=node.countCurMonitorObjs(conditions)
        
        self.traverseDown(dealFun)
        return rs
    
    @classmethod
    def findByPath(cls, path):
        "根据节点路径返回节点对象，如果没有找到返回None"
        findNode = {"ret":None}
        def dealFun(node):
            if path == node.getPath():
                findNode["ret"] = node
                return False
        
        root = cls.getRoot()
        if root:
            root.traverseDown(dealFun)
        return findNode["ret"]
    
    def listAllNodes(self, includeSelf=True):
        """
        把所有的节点（包括本身 includeSelf=True），转换为list
        @return: list
        """
        rs = []
        def dealFun(node):
            rs.append(node)
        
        self.traverseDown(dealFun)
        if not includeSelf and rs: del rs[0]
        return rs
    
    def listSubNodes(self):
        nodes = self._getRefMeObjects('parent', self.__class__, conditions={})
        return nodes
        
    def addChild(self, childNode):
        """
            为当前节点添加子节点
            @param  childNode:子节点
        """
        childNode.parent = self
        childNode.ownCompany = self.getRoot().ownCompany
        return self
        
    def isChild(self, childNode):
        """
            判断childNode是否是当前节点的子节点
            @return: 是则返回True,不是则返回False
        """
        ret = {
            "isChild":False,
        }
        uname = childNode.uname
        
        def dealFun(node):
            if node.uname == uname:
                ret["isChild"] = True
                return False
        self.traverseDown(dealFun)
        if ret["isChild"]:
            return True
        return False
        

        
    def isRoot(self):
        """
                判断当前对象是否是根对象
        """
        if self.uname == self.rootName:
            return True
        return False
    
    def remove(self):
        """
            递归删除当前对象构成的子树，根节点对象保留不删除
            @return:返回删除中遇到的错误
        """
        allNodes = self.listAllNodes()
        allNodes.reverse()
        for node in allNodes:
            if node.getPath() == '/' + self.__class__.rootUname: continue #根节点
            DocModel.remove(node)
        
    def traverseDown(self, dealFun):
        """
            向下递归遍历树
            @param dealFun:  每次执行的函数
               该函数带有一个本对象类型的参数，如果该函数返回False，则终止递归
        """
        fg = dealFun(self)
        if fg == False:return
        
        for item in self.items:
            item.traverseDown(dealFun)
            
    
    def _toDict(self, fillDictFun=None):
        _dict = {
                 "_id": self.getUid(),
                 "title":self.titleOrUid(),
                 "uname": self.uname,
                 "path": self.getPath(),
                 "_type": self.__class__.__name__
        }
        
        
        for node in self.items:
            if not _dict.has_key('items'): _dict["items"] = []
            
            childDict = node._toDict(fillDictFun)
            _dict['items'].append(childDict)
        
        #----------------------------------------------------
        if fillDictFun:
            fd = fillDictFun(self)
            if fd and fd.has_key('items') and fd['items']:
                _dict['items'] = _dict.get('items', [])
                _dict['items'].extend(fd.get('items'))
                
            if fd.has_key('items'): del fd['items']   
            _dict.update(fd)
            
        return _dict
        
    def traverseUp(self, dealFun):
        """
            向上递归遍历树
            @param dealFun:  每次执行的函数
               该函数带有一个本对象类型的参数，如果该函数返回False，则终止递归
        """
        fg = dealFun(self)
        if fg == False:return
        
        if hasattr(self, 'parent') and self.parent: 
            self.parent.traverseUp(dealFun)
        else: return 
    
        

    
    


