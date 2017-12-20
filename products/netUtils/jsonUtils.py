#coding=utf-8

__doc__ = """
方法起名规范 def jsonXXX(obj)：
注XXX 是类名
"""

from copy import deepcopy

def jsonDoc(obj, updict={}, ignoreProperyties=[]):
    objDict = deepcopy(obj._medata)
    for pn in ignoreProperyties:
        if objDict.has_key(pn): del objDict[pn]
    
    objDict["_id"] = str(objDict.get("_id",""))
    objDict["title"] = obj.titleOrUid()
    objDict.update(updict)
    return objDict
    
def jsonDocList(objList, updict=None, ignoreProperyties=[]):
    rs = []
    for obj in objList: 
        _updict = {}
        if updict:
            _updict = updict(obj) #updict is function
        rs.append(jsonDoc(obj, updict=_updict, ignoreProperyties=ignoreProperyties))
    return rs




