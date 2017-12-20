#coding=utf-8
import md5
from products.netModel.user.user import User

class NetBaseBackend(object):
    def authenticate(self, username=None, password=None):
        userObj = User._loadByUserName(username)
        if userObj: userObj.id = userObj.getUid()
        
        if userObj and userObj.password == md5.new(password).hexdigest():
            return  userObj
        return None
    
    def get_user(self, user_id):
        return User._loadObj(user_id)
        
                