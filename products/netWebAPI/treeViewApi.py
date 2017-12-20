#coding=utf-8

from products.netPublicModel.modelManager import ModelManager as MM
from products.netWebAPI.base import BaseApi
from products.netPublicModel.userControl import UserControl
from products.netModel.org.location import Location

#--------------------------------------------------------------------------------------------------#    
def _fillDictFun(node, conditions):
    """
    包涵监控对象节点的树结构
    """
    curMonitorObjs = node.getCurMonitorObjs(conditions=conditions)
    _dict = {'items':[]}
    for mo in curMonitorObjs:
        _type = mo.__class__.__name__
        _dict['items'].append({'title': mo.titleOrUid(), '_id': mo.getUid(), '_type':_type})
    return _dict


def _fillDictFun22(node, conditions):
    """
    不包涵监控对象节点的树结构
    """
    objs = node.getAllMonitorObjs(conditions=conditions)
    _dict = {'count':len(objs)}
    return _dict


def _fillLocDictFun(node, conditions, allowTypes=[]):
    "不包涵对象的填充方法"
    c = node.countAllMonitorObjs(conditions=conditions, allowTypes=allowTypes)
    _dict = {'items':[], "count":c["sum"]}
    return _dict

def _fillLocDictFun2(node, conditions, allowTypes=[]):
    "包涵对象的填充方法"
    curMonitorObjs = node.getCurMonitorObjs(conditions=conditions, allowTypes=allowTypes)
    _dict = {'items':[]}
    for mo in curMonitorObjs:
        _type = mo.__class__.__name__
        _dict['items'].append({'title': mo.titleOrUid(), '_id': mo.getUid(), '_type':_type})
    return _dict
#--------------------------------------------------------------------------------------------------#

class TreeViewApi(BaseApi):
    
    def getHostTreeDataSource(self):
        dr = MM.getMod('dataRoot')
        deviceClsRoot = dr.getOrgRoot('DeviceClass')
        conditions = {}
        UserControl.addCtrlCondition(conditions)
        
        ds = deviceClsRoot._toDict(lambda node: _fillDictFun(node, conditions))
        #ds = deviceClsRoot._toDict()
        return [ds]
    
    
    def getHostTreeWithLocDataSource(self):
        "带分组的主机树"
        dr = MM.getMod('dataRoot')
        deviceClsRoot = dr.getOrgRoot('DeviceClass')
        conditions = {}
        locConditions={}
        UserControl.addCtrlCondition(conditions)
        UserControl.addCtrlCondition(locConditions)
        
        locs = Location._findObjects(conditions=locConditions)
        ds = []
        for  loc in locs:
            _locDs = {"_id":loc.getUid(), "title":loc.titleOrUid(), "_type":loc.__class__.__name__,"expanded":False}
            conditions.update({"location":loc._getRefInfo()})
            _ds = deviceClsRoot._toDict(lambda node: _fillDictFun22(node, conditions))
            _locDs["items"]=_ds.get("items",[])
            ds.append(_locDs)
        return ds
    
    
    
    
    
    
    
    def getNetworkTreeDataSource(self):
        dr = MM.getMod('dataRoot')
        deviceClsRoot = dr.getOrgRoot('NetworkClass')
        conditions = {}
        UserControl.addCtrlCondition(conditions)
        
        ds = deviceClsRoot._toDict(lambda node: _fillDictFun(node, conditions))
        
        def _mf(d3):
            if d3.get("count", []):return True
            return False
            
        for d2 in ds["items"]:
            d3s = filter(_mf, d2["items"])
            d2["items"] = d3s
            
        return [ds]
    
    def getNetworkTreeDataSource2(self):
        dr = MM.getMod('dataRoot')
        deviceClsRoot = dr.getOrgRoot('NetworkClass')
        conditions = {}
        UserControl.addCtrlCondition(conditions)
        
        ds = deviceClsRoot._toDict(lambda node: _fillDictFun22(node, conditions))
        
        def _mf(d3):
            if d3.get("count", 0):return True
            return False
            
        for d2 in ds["items"]:
            d3s = filter(_mf, d2["items"])
            d2["items"] = d3s
            
        return [ds]
    
    def getWebsiteTreeDataSource(self):
        dr = MM.getMod('dataRoot')
        root = dr.getOrgRoot('WebSiteClass')
        ds = root._toDict(lambda node: _fillDictFun(node, {}))
        return [ds]
    
    
    def getMiddlewareTreeDataSource(self):
        dr = MM.getMod('dataRoot')
        root = dr.getOrgRoot('MiddlewareClass')
        ds = root._toDict(lambda node: _fillDictFun(node, {}))
        return [ds]
    
    def getVmhostTreeDataSource(self):
        dr = MM.getMod('dataRoot')
        vmhostClsRoot = dr.getOrgRoot('VmhostClass')
        conditions = {}
        UserControl.addCtrlCondition(conditions)
        
        ds = vmhostClsRoot._toDict(lambda node: _fillDictFun(node, conditions))
        #ds = deviceClsRoot._toDict()
        return [ds]

    def getLocationDevTreeDataSource(self, allowTypes=[]):
        "不包涵对象的位置树结构"
        dr = MM.getMod('dataRoot')
        root = dr.getOrgRoot('Location')
        ds = root._toDict(lambda node: _fillLocDictFun(node, {}, allowTypes=allowTypes))
        return [ds]
    
    
    def getLocationDevTreeDataSource2(self, allowTypes=[]):
        "包涵对象的位置树结构"
        dr = MM.getMod('dataRoot')
        root = dr.getOrgRoot('Location')
        ds = root._toDict(lambda node: _fillLocDictFun2(node, {}, allowTypes=allowTypes))
        return [ds]
    
        
    
if __name__ == "__main__":

    t = TreeViewApi()
    print t.getWebsiteTreeDataSource()
        
