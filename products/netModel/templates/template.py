#coding=utf-8
from products.netModel.baseModel import DocModel
from products.netModel.templates.ds import BaseDataSource
from products.netModel import medata
   
class Template(DocModel):
    """ 
    模板
    模板的作用是定义了被监控对象可采集的数据内容，
    及采集数据的方式(snmp,command),以及数据点的阀值的界定
    """
    dbCollection = 'Template'
    
    def __init__(self , uid=None):
        DocModel.__init__(self)
        self._medata.update(dict(
            _id = uid,
            dataSources = {}
        ))


        
    isBaseTpl = medata.plain("isBaseTpl", False) #基础模板?
    
    tplType = medata.plain("tplType", "base") #base-基础模板 extend-扩展模板 customer-自定义模板
    
    @property
    def uname(self):
        return self.getUid()
    

    
    @property
    def _dataSources(self):
        """
            获取数据源medata
            @return: <dict>
        """
        return self._medata.get('dataSources')
               
    def getDataSource(self, dsName):
        """
        通过数据源名称，返回一个数据源实例
        @param dsName: <string> 据源名称
        @return: <object>数据源
        """
        dsMedata = self._medata['dataSources'].get(dsName, None)
        if not dsMedata: return None
        return BaseDataSource.createInst(dsMedata)
    
    def addDataSource(self, ds):
        """
            添加一个数据源
            @param ds: 数据源 type->BaseDataSource的子类对象
        """
        if not ds.uname:
            raise Exception('Datasource uname can not be empty!')
        
        self._dataSources[ds.uname] = ds._medata
        self._commUpdate({"$set":{"dataSources.%s" % ds.uname: ds._medata}})
        return self
    
    def deleteDataSource(self, dsName):
        """
            删除一个数据源
            @param dsName: 数据源名称 type->string 
        """
        if dsName in self._dataSources:
            del self._dataSources[dsName]
            
        self._commUpdate({"$unset":{"dataSources.%s" % dsName:1}})
        return self
    
    def findDataSources(self, typeStr=None):
        """
        通过类型，筛选数据源
        typeStr=None 获取所有的数据源
        @param typeStr: type->String  数据源类型 SnmpDataSource|CmdDataSource|WmiDataSource
        @return: Dict <{dsName:<Dataource>}>
        """
        dss = {}
        
        if typeStr is None: #get all
            for dsName, dsMedata in self._dataSources.items():
                ds = BaseDataSource.createInst(dsMedata)
                if ds: dss[dsName] = ds
            return dss
        
        #find by type
        for dsName, dsMedata in self._dataSources.items():
            if dsMedata["type"] == typeStr: 
                ds = BaseDataSource.createInst(dsMedata)
                if ds: dss[dsName] = ds
            
        return dss
    
    @property
    def thresholds(self):
        """
            获取所有阀值字典
            @return: <dict> {tplName|dsName|dpName|thName:medata}
            @return: <dict> {template:{ds:{dp:{th:{medata}}}}}
        """
        thresholds = {}
        
        tplName = self.getUid()
        for dsName in self._dataSources:
            ds = self.getDataSource(dsName)
            for dpName in ds.dataPoints:     
                dp = ds.getDataPoint(dpName)
                if not dp._thresholds:continue               
                for threshold in dp._thresholds:
                    thName = dp._thresholds[threshold].get("uname")
                    thdKey = "%s|%s|%s|%s" %(tplName,dsName,dpName,thName)
                    thresholds[thdKey]=dp._thresholds[threshold]
        return thresholds
      
        
        

    

    
    
        
        
