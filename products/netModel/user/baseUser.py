#coding=utf-8
from products.netModel.centerDocModel import CenterDocModel
from products.netModel import medata
class BaseUser(CenterDocModel):
    def __init__(self, uid=None):
        CenterDocModel.__init__(self)
        self._medata.update(dict(
            _id=uid, 
            is_active=False,
        ))
      

    createTime = medata.plain("createTime", 0) #0表示未创建, 创建时=time.time()
    email = medata.plain("email","")
    contactPhone = medata.plain("contactPhone", "")
    password = medata.plain("password")
    username = medata.plain("username","")
    originalName = medata.plain("originalName","") #真实名
    last_login = medata.plain("last_login", 0) #0表示未创建, 创建时=time.time()
    icon = medata.plain("icon","") #头像
    sign = medata.plain("sign", "") #个性签名

    
    @classmethod
    def _loadByUserName(cls, username):
        conditions = {"username":username}
        users = cls._findObjects(conditions=conditions)
        if users: return users[0]
        return None
    
    def titleOrUid(self):
        return self.originalName or  self.username or self.getUid()
    
    
    def save(self):
        "Do not del this method, it's created for django"

    def is_authenticated(self):
        "Do not del this method, it's for django"
        return True

    @property
    def is_active(self):
        return self._medata["is_active"]
    

    
