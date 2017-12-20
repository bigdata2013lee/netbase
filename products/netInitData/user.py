#coding=utf-8
from products.netModel.company import Company
from products.netModel.user.user import User

def initCompanys():
    
    c = Company("netbase")
    c.title = "safedragon.com"
    c._saveObj()
    return c
    
def initUser():
    if  Company._loadObj("netbase") is None:
        company = initCompanys()
    else:
        company = Company._loadObj("netbase")
           
    u = User("admin")
    
    u.password = "admin"
    
    u.email = "cqz@safedragon.com.cn"
    
    u.ownCompany=company
    u._medata["is_active"] = True
    u._saveObj()
    return u
    
    
if __name__ == "__main__":
    initUser()
    