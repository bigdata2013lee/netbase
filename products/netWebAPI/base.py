#coding=utf-8


def apiAccessSettings(name, module="nbGlobal"):
    """
    作为装饰器，设置Api方法的访问控制属性
    @param name: add, del, edit, view
    @param module:业务模块名，可根据需要分配一个特定的名称
    """
    def  _deco(fun):
        def _deco2(*args, **kws):
            ret = fun(*args, **kws)
            return ret
        _deco2.accessSettings = dict(name=name, module=module)
        return _deco2
    return _deco

class BaseApi(object):
    
    def __init__(self):
        self.request = None
