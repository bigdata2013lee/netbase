# -*- coding: utf-8 -*-
from products.netModel.templates.template import Template
from products.netModel.templates.performImage import PerformImage, ImagePoint
import time
from products.netUtils import xutils
from products.netWebAPI.base import BaseApi


class PerformImageApi(BaseApi):
        
    def getTemplateDs(self, tplUid):
        tpl = Template._loadObj(tplUid)
        
        dss = {}
        for dsName, ds in tpl.dataSources.items():
            dss[dsName] = ds._toDict()
            
        return dss
    
      
    def getPerImagePoint(self, tplUid, perImgUid, uname):
        """
        获取图像点
        @param perImgUid: 图UID
        @param uname: 图像点名
        """
        perImgObj = PerformImage._loadObj(perImgUid)
        iPoint = perImgObj.imagePoints[uname]
        if iPoint: return iPoint.toDict()
    
      
    def delPerImagePoint(self, perImgUid, uname):
        perImgObj = PerformImage._loadObj(perImgUid)
        if not perImgObj:
            return "FAIL"
        perImgObj.deleteImagePoint(uname)
        return "OK"
    
      
    def savePerImagePoint(self, perImgUid, uname, dsName, dpName, type, color, lineWidth, unit):   
        perImgObj = PerformImage._loadObj(perImgUid)
        if not perImgObj:
            return "FAIL"
            
        iPoint = ImagePoint(uname)
        iPoint.dsName = dsName
        iPoint.dpName = dpName
        iPoint.type = type
        iPoint.color = color
        iPoint.lineWidth = lineWidth
        iPoint.unit = unit
        perImgObj.addImagePoint(iPoint)
        
        return "OK"
    
    
    def savePerImg(self, tplUid, title, description):
        u"""
            新增一个性能图
        """
        perImg = PerformImage()
        perImg.title = title
        perImg.description = description
        tpl = Template._loadObj(tplUid)
        perImg._saveObj()
        perImg.template = tpl 
        return "OK"
    
    
    def delPerImg(self, perUid):
        perImg = PerformImage._loadObj(perUid)
        if perImg:
            perImg.remove()
        return "OK"
    
        
    
    def getAllPerImgs(self, deviceUid):
        from products.netPerData import manager as perDataMgr
        dr = xutils.getDataRoot()
        dev = dr.findDeviceByUid(deviceUid)
        rs = perDataMgr.getDevicePerImgConfigs(dev)
        return rs
        
    
    def getDevicePerImgDataSource(self, deviceUid, perImgUid):
        from products.netPerData import manager as perDataMgr
        dr = xutils.getDataRoot()
        dev = dr.findDeviceByUid(deviceUid)
        perImgObj = PerformImage._loadObj(perImgUid)
        minVal = 1
        end = int(time.time())
        start = end - 3600 * 24 * 7 #7天
        return perDataMgr.getDevicePerImgDataSource(dev, perImgObj, start, end, minVal)
        
    
