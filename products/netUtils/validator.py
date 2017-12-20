#coding=utf-8
import types

import re
        
class Validator(object):
    def __init__(self, rules={}, messages={}):
        self.rules=rules
        self.messages=messages
        
    
    def v(self, params={}):
        fg  = True
        for k,v in params.items():
            vMethod = self.rules.get(k, None)
            if vMethod and  type(vMethod)==types.FunctionType :
                fg = vMethod(v);
                if not fg:
                    return False, self.messages.get(k,"")
                
            elif vMethod and  type(vMethod) in types.StringTypes :
                _vMethod = getattr(Validator, vMethod, None)
                fg = _vMethod(v)
                if not fg:
                    return False, self.messages.get(k,"")
                
            elif vMethod and  type(vMethod) == types.DictType :
                dd=vMethod
                _vMethod = getattr(Validator, vMethod.get("rule",None), None)
                del dd["rule"]
                fg = _vMethod(v, **dd)
                if not fg:
                    return False, self.messages.get(k,"")
                
                
        return True, ""
    
            
    @classmethod
    def required(cls, val):
        if val and  type(val) in types.StringTypes:
            return val.strip()
        return val
    
    @classmethod
    def maxLength(cls, val, max=1):
        return len(val)>=max
        
    @classmethod
    def minLength(cls, val, max=1):
        return len(val)<=max

    @classmethod
    def inRange(cls, val, min=0, max=100):
        return min <= val <= max
    
    @classmethod
    def inArray(cls, val, array=[]):
        return val in array
    
    @classmethod
    def notInArray(cls, val, array=[]):
        return val not in array
            
    @classmethod
    def regex(cls, val, regex=None):
        print regex
        if re.match(regex, val): return True
        return False
        
    @classmethod
    def email(cls, val):
        if re.match(r"^[0-9a-zA-Z_\.#]+@(([0-9a-zA-Z]+)[.])+[a-z]{2,4}$", val): return True
        return False
    
    @classmethod
    def ipAddress(cls, val):
        if re.match(r"^\s*\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\s*$", val): return True
        return False
    
    @classmethod
    def url(cls, val):
        if re.match(r"^[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+\.?$", val): return True
        return False
    
    @classmethod   
    def macAddress(cls, val):
        if re.match(r"^\s*([0-9a-fA-F]{2,2}:){5,5}[0-9a-fA-F]{2,2}\s*$", val): return True
        return False
            
if  __name__ == "__main__":
    
    def  maxAge(val):
        return 1 <= val <=150
    
    rules={
           "title":"required",
           "username":"email",
           "mylist": {"rule":"maxLength", "max":4},
           "password": {"rule":"regex", "regex":"\w{4,20}"},
           "age": {"rule":"inRange","min":1, "max":150},
    }
    
    messages={
           "title":"标题是必填项",
           "username":"邮件格式不正确",
           "mylist":"请选择至少3个项目",
           "password":"密码不能包涵特殊字符",
           "age":"年龄输入在1~150之间",
    }
    
    params={
            "title":"0000",
            "username":"12345@6163.com",
            "mylist":[1,2,3,4],
            "password":"100001",
            "age":50,
    }
    rs  = Validator(rules=rules, messages=messages).v(params)
    
    print "%s:%s" %rs
    
    
    
    
    
            