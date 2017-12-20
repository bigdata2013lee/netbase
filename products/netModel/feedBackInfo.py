import time
from products.netModel.baseModel import DocModel
from products.netModel import medata


def getCurrentDate():
    data=time.time()
    st=time.localtime(data)
    return time.strftime("%Y-%m-%d %H:%M:%S",st)

class FeedBackInfo(DocModel):
    dbCollection = 'FeedBackInfo'
    def __init__(self):
        DocModel.__init__(self)

    infoTime = medata.plain("infoTime", getCurrentDate())
    feedBackUser = medata.plain("feedBackUser", "")
    feedBackEmail = medata.plain("feedBackEmail", "")
    feedBackContent = medata.plain("feedBackContent", "")