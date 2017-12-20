#coding=utf-8
'''
Created on 2014-4-2

@author: llh
'''
__doc__="不影响系统运行和用户数据的前提下修改数据库使用该脚本，根据每次修改的不同脚本会有变动"


from products.netModel.company import Company
from products.netModel.collector import Collector



def main():
    colls = Collector._findObjects()
    for c in colls:
        cpy = Company()
        cpy.title = "润迅"
        cpy._saveObj()
        cpy._saveProperty2("isIdc", True)
        c._saveProperty2("ownIdc",cpy.title)
    
if __name__ == "__main__":
    main()