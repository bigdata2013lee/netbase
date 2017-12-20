#coding=utf-8

class Conf(object):
    pass

#建议、合理配置值在600-900间，并建议pefValueTimeRange、statusValueTimeRange值一致
#默认值600,不建议修改
Conf.selectTimeRange={
    "pefValueTimeRange":900,
    "statusValueTimeRange":900
}

#收集器容量
Conf.colloectorCapacity={
    "defaults":500,
    "Device":500,
    "Website":500,
    "Network":400
}

Conf.demo={
    "demoUserName":"demo@safedragon.com.cn",
    "demoPwd":"fe01ce2a7fbac8fafaed7c982a04e229",
    "demoEmail":"demo@safedragon.com.cn",
}

Conf.emails={
             "upLevelReceiveEmail":"cqz@safedragon.com.cn",
             "updatePersonalInfoMail":"cqz@safedragon.com.cn",
}

#-----------------------------------------------------------------#
def get(sec, opt, defaultVal=None):
    sec_conf = getattr(Conf, sec)
    return sec_conf.get(opt, defaultVal)
    
    
    
