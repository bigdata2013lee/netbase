#coding=utf-8
import types
import time
import medata
from products.netModel import  mongodbManager as dbManager
from products.netUtils import xutils
from products.netModel.cacheManager import CacheModel


class BaseModel(object):
    def __unicode__(self):
        """@功能：当前节点的说明"""
        return self.title

class DocModel(CacheModel, BaseModel):

    def __init__(self):
        self._medata = {"_id":None, "title":""}
        self.__initMedata()
        
    @classmethod
    def __getMpropertys(cls):
        propertys = []
        for proName in dir(cls):
            if proName.find("_") == 0:continue
            pro = getattr(cls, proName)
            if isinstance(pro, medata.MedataProperty):
                propertys.append(pro)
        return propertys
    
        
    def __initMedata(self):
        mPros = self.__getMpropertys()
        _medata = {}
        for pro in mPros:
            _medata[pro.medataName] = pro.defaultVal
            
        self._medata.update(_medata)
        
    @property
    def title(self):
        return self._medata['title']

    @title.setter
    def title(self, title):
        self._medata["title"] = title
        self._saveProperty("title")

    def getUid(self):
        """
        @功能：得到当前对象的唯一标示
        @返回：字符串类型的唯一标示
        """
        if not self._medata.get("_id", None): return None
        return str(self._medata['_id'])

    def titleOrUid(self):
        return self.title or self.getUid()

    def __extMedata__(self, properties):
        self._medata.update(properties)

    def __eq__(self, other):
        if isinstance(other, DocModel):
            return self.getUid() == other.getUid()
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, DocModel):
            return self.getUid() != other.getUid()
        return True

    def _saveObj(self):
        """
        保存对象数据到mongodb数据库
        """
        if not self.dbCollection: raise Exception("静态属性dbCollection不存在， 请指明保存的表名")
        table = self._getDbTable()
        if not self._medata.get("_id", None): del self._medata["_id"]
        table.save(self._medata) #'_id' will be set in _medata

        self._c_setObj(self)
        self.__after_saveObj__()

        return self

    def __after_saveObj__(self):
        "此方法由_saveObj(第一次保存对象时)调用，适用于保存一些初始化、默认的属性至库中"
        pass

    def _saveProperty(self, pros=[]):
        """
            同步当前对象中的属性到数据库
            可以同步单个属性，也可以同步多个属性
            @param pros: 需要同步的属性
        """
        if not self.getUid(): return
        prosMap = {}
        if type(pros) in types.StringTypes: pros = [pros]
        for pName in pros:
            prosMap.update({pName: self._medata.get(pName, None)})
        if prosMap:
            table = self._getDbTable()
            table.update({'_id': xutils.fixObjectId(self.getUid())}, {'$set': prosMap})
            self._c_setObj(self)

    def _saveProperty2(self, pn, pv):
        """
        _saveProperty2
        """
        prosMap = {pn:pv}
        if pv and isinstance(pv, DocModel): prosMap = {pn:pv._getRefInfo()} 
            
        self._medata.update(prosMap)
        if not self.getUid(): return
        if pv and isinstance(pv, DocModel):
            self._saveDocProperty(pv, pn)
            return

        table = self._getDbTable()
        table.update({'_id': xutils.fixObjectId(self.getUid())}, {'$set': prosMap})
        self._c_setObj(self)

    def _saveDocProperty(self, doc, pName):
        """
        保存文档引用对象
        """
        if not doc:
            self._medata[pName] = None
        else:
            self._medata[pName] = doc._getRefInfo()

        self._saveProperty(pName)

    def _commUpdate(self, updateDict):
        "通用的数据操作方法，通过自定义updateDict，实现灵活的修改操作"
        table = self._getDbTable()
        table.update({'_id': xutils.fixObjectId(self.getUid())}, updateDict)
        self._c_setObj(self)


    @classmethod
    def _getDbTable(cls):
        """
            得到当前对象的mongodb集合表
        """
        db = dbManager.getNetbaseDB()
        table = getattr(db, getattr(cls,"dbCollection","") or cls.__name__)
        return table


    @classmethod
    def _loadObj(cls, uid=None, cached=True):
        """
            通过uid从mongdb中加载所有属性
            @param uid：uid 唯一标示
        """
        
        if cached:
            inst = cls._c_loadObj(uid)
            if inst:
                #print "log: get obj %s from cache." %uid
                return inst
                
            
        inst = cls()
        if uid: inst._medata['_id'] = xutils.fixObjectId(uid)
        if not inst.getUid(): return None
        table = cls._getDbTable()
        data = table.find_one({'_id': inst._medata['_id']})

        if data:
            #print "log: get obj %s from mongo." %uid
            inst._medata = data
            cls._c_setObj(inst)
            return inst
        return None

    @classmethod
    def _loadObjFromMap(cls, medata):
        """
            从medata中设置对象的属性
            @param medata:字典类型
        """
        obj = cls()
        obj._medata = medata
        cls._c_setObj(obj)
        return obj



    def remove(self, safe=None):
        """
        功能：通过当前对象的_id 删除当前对象
        """
        dbTable = self._getDbTable()
        dbTable.remove({"_id": xutils.fixObjectId(self.getUid())}, safe=safe)
        self._c_delObj(self)


    def _getRefInfo(self):
        """
        得到当前对象的序列化唯一标示
        """
        return RefDocObject.getRefInfo(self)

    def _getRefMeObjects(self, propertyName, cls, conditions={}, sortInfo=None, skip=0, limit=None):
        """
                引用self的关联对象列表
        @param cls: 引用类
        @param propertyName: 引用属性
        @param conditions: 附加过滤条件
        """
        refInfo = self._getRefInfo()
        tb = cls._getDbTable()
        cds = {propertyName: refInfo}
        cds.update(conditions)
        objs = []
        cursor = tb.find(cds)
        if skip: cursor.skip(skip)
        if limit: cursor.limit(limit)
        if sortInfo: cursor.sort(sortInfo.items())
        for data in cursor:
            obj = cls._loadObjFromMap(data)
            objs.append(obj)

        return objs

    @classmethod
    def _findObjects(cls, conditions={}, sortInfo=None, skip=0, limit=None):
        "_findObjects"
        dataObjs = []
        objects = []

        cursor = cls._getDbTable().find(conditions)
        if sortInfo: cursor.sort(sortInfo.items())
        if skip: cursor.skip(skip)
        if limit: cursor.limit(limit)

        for obj in cursor: dataObjs.append(obj)

        for obj in dataObjs:
            clsInst = cls._loadObjFromMap(obj)
            objects.append(clsInst)

        return objects
    
    @classmethod
    def _countObjects(cls, conditions={}):
        """
        根据条件，统计对象列表的数量
        @param conditions: <dict> 查询条件
        @return: int
        """
        return cls._getDbTable().find(conditions).count()
    
    @classmethod
    def _minRefMeCount(cls, conditions={}):
        rs = cls._getDbTable().group(['collector'],conditions,{"sum":0 }, reduce = """function(doc, prev){prev.sum ++}""")
        return RefDocObject.getInstance(rs[-1]['collector']), rs[-1]["sum"]
    
class BaseComponentModel(DocModel):
    
    def __init__(self):
        DocModel.__init__(self)
        self.__extMedata__(dict(
            createTime=time.time(),
        ))
     
    collector = medata.doc("collector") #收集器
    ownCompany = medata.doc("ownCompany") #公司
    description = medata.plain("description","")
    
    @property
    def creatTime(self):
        return self._medata.get("createTime")
     
    @classmethod    
    def getComponentType(cls):
        return cls.__name__
    


    def getManageId(self):
        """
        获取对象的管理Id
        """
        #raise Exception("Method:getManageId must be overwrite in subclass.")
        return ""
    
    @property
    def createTime(self):
        return RefDocObject.getInstance(self._medata['createTime'])

    def titleOrUid(self):
        return self.title or self.getManageId() or self.getUid()
    

    
class RefDocObject(object):

    @staticmethod
    def getRefInfo(docObj):
        """
        得到docObj对象的序列化唯一标示
        """
        if not docObj.getUid(): raise Exception("Create Ref info exception")
        return "refid:%s;cls:%s" % (str(docObj.getUid()), str(docObj.__class__))

    @staticmethod
    def isRefObj(refObj):
        """
            判断refObj字符串是否是序列化的字符串对象
            @return： 是则返回数组（id,类名），不是则返回False
        """
        if not refObj: return False
        if type(refObj) not in types.StringTypes:return False
        import re
        pattern = r"^refid:([\w\-\.]+);cls:<class\s+'(.+)'>$"
        patternObj = re.compile(pattern, flags=0)
        m = patternObj.match(refObj)
        if not m: return False
        return m.group(1), m.group(2)

    @staticmethod
    def getInstance(refObj):
        """
            如果refObj可以反序列化则通过refObj反序列化为对象，否则不做处理
            @param refObj: 序列化的对象字符串
            @return: 如果反序列化成功则返回反序列化的对象, 否则返回其refObj
        """
        rsIsRefObj = RefDocObject.isRefObj(refObj)
        if not rsIsRefObj: return refObj
        clsInst = xutils.importClass(rsIsRefObj[1])
        inst = clsInst._loadObj(rsIsRefObj[0])
        return inst

    @staticmethod
    def instRefList(refList):
        objs = []
        for obj in refList:
            _obj = RefDocObject.getInstance(obj)
            objs.append(_obj)
        return objs



if __name__ == '__main__':
    from products.netModel.middleware.mwNginx import MwNginx
    rs = MwNginx._minRefMeCount()
    print rs
















