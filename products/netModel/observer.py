'''
Created on 2012-12-10

@author: Administrator
'''

class Observer(object):


    def __init__(self):
        '''
        Constructor
        '''
        self._events_ = {}
    
    def fireEvent(self, ename, **kw):
        "fireEvent"
        eList = self._events_.get(ename,[])
        for handler in eList: handler(**kw)
        
    def un(self,ename, handler):
        "un"
        eList = self._events_.get(ename,[])
        for i in xrange(len(eList)-1, -1, -1):
            if eList[i] == handler: del eList[i]
        
            
    def on(self,ename, handler):
        "on"
        eList = self._events_.get(ename,[])
        if not eList: self._events_[ename] = eList
        eList.append(handler)
        
    def one(self,ename, handler):
        "one"
        
        
        
        
        