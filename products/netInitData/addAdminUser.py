#coding=utf-8


from products.netModel.user.adminUser import AdminUser

def addAdminUser():
    import hashlib
    admin = AdminUser("admin")
    admin.password = hashlib.md5("admin").hexdigest()
    admin.email = "admin@safedragon.com.cn"
    admin._medata["is_active"] = True
    admin._saveObj()


if __name__ == "__main__":
    
    addAdminUser()
    
