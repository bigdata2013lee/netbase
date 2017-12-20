#coding=utf-8

from products.netModel.collector import Collector

def initCollcetors():
    #初始化内建收集器
    coll = Collector()
    data = {
         "_id":"public_coll_001",
          "host": "127.0.0.1",
          "ownCompany": None,
          "status": True,
          "title": "public coll 001"
        }
    coll.__extMedata__(data)
    coll._saveObj()


if __name__ == "__main__":
    initCollcetors()
    
        
    
