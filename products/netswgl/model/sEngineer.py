#coding=utf-8
from products.netModel import medata
from products.netswgl.model.swglDocModel import SwglDocModel

class SEngineer(SwglDocModel):
    "服务商-认证专家工程师"
    
    dbCollection = 'SEngineer'
    
    def __init__(self, uid=None):
        SwglDocModel.__init__(self)
        self._medata.update(dict(
            _id=uid, 
        ))

    #姓名使用title属性
    personalID = medata.plain("personalID", "") #身份证号码
    identityCardPath= medata.plain("identityCardPath", "") #身份证
    ownServiceProvider= medata.doc("ownServiceProvider") #所属服务提供商
    phone= medata.plain("phone", "") #电话
    qq= medata.plain("qq", "") #qq
    email= medata.plain("email", "") #公司邮箱
    goodKillsAt= medata.plain("goodKillsAt", "") #技术特长
    ipmpi= medata.plain("ipmpi", "") #专业资质认证 International Project Management Profe ional
    ipmpiPath= medata.plain("ipmpiPath", "") #专业资质认证
    
    cpcAddr=medata.plain("cpcAddr", {"r0":"0", "r1":""}) #地址/省、市 代码
    domain=medata.plain("domain", {"d0":"1", "d1":"1_1"}) #领域方向
    
    warmHeartRate= medata.plain("warmHeartRate", 50) #热心度 1-3
    solveRate= medata.plain("solveRate", 50) #解决率 1-3
    technicalRate= medata.plain("technicalRate", 50) #专业性 1-3
    timeEfficientRate= medata.plain("timeEfficientRate", 50) #时效性 1-3
    
    goodRate= medata.plain("goodRate", 50) #综合好评率 0-100,  由上面几个Rate平均值
    
    #记录评论的人次，以便统计得分
    #算法 (正-负)/总*100% + 平/总*50%
    pljl = medata.plain("pljl", {
                                     "warmHeart-":1, "warmHeart":1, "warmHeart+":1, 
                                     "solve-":1, "solve":1, "solve+":1, 
                                     "technical-":1, "technical":1, "technical+":1,
                                     "timeEfficient-":1, "timeEfficient":1, "timeEfficient+":1})
    
    
    def updateRates(self):
        "更新评价指标"
        pljl = self.pljl
        
        def _xx(name):
            z = pljl.get("%s+" %name, 1) 
            f =  pljl.get("%s-" %name, 1) 
            p = pljl.get("%s" %name, 1)
            
            all = float(z+f+p)
            
            x = (z/all)*100
            return int(x)
        
        self.warmHeartRate = _xx("warmHeart")
        self.solveRate = _xx("solve")
        self.technicalRate = _xx("technical")
        self.timeEfficientRate = _xx("timeEfficient")
        
        self.goodRate = (self.warmHeartRate + self.solveRate + self.technicalRate + self.timeEfficientRate) / 4
        
        self._saveObj()
            
            
            
        
        
        
        
    
