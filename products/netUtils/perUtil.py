#coding=utf-8

class perTransformUnits(object):
    
    @staticmethod
    def one(val):
        return val
    
    @staticmethod
    def ten(val):
        return val
    
    @staticmethod
    def hundred(val):
        return val
    
    @staticmethod
    def thousand(val):
        return val
    
    @staticmethod
    def kb(val):
        return val / 1024
    
    @staticmethod
    def mb(val):
        return val / 1024 / 1024
    
    @staticmethod
    def percentage(val):
        return val * 100
    
    
perTransformUnits.names = {
    "one": "个", "ten":"十", "hundred": "百", "thousand": "千", 
    "kb": "Kb", "mb": "Mb", "percentage": "%"
}



 
    