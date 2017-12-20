#coding=utf-8
import os
import md5
version="2.2"
oldMd5="3d7702380c56f091e8d39b5e932421bb"
def getVersion():
    nowMd5=getFileMD5()
    print nowMd5
    if oldMd5==nowMd5:
        return "当前版本是%s"%version
    else:
        return "该版本已被修改,版本未知!"

def getFileMD5():
    """
        得到软件的MD5校验码(通过判断文件是否一致,没有有修改过)
    """
    m = md5.new()
    rpath="%s/products" %(os.environ["NBHOME"])
    for root,dirs,files in os.walk(rpath):
        for filespath in files:
            if not (filespath.endswith(".py") or 
                    filespath.endswith(".js") or
                    filespath.endswith(".css")):
                continue
            fileName=os.path.join(root,filespath)
            f = open(fileName,'rb')
            m.update(f.read())
            f.close()
    return m.hexdigest()
            
            
if __name__=="__main__":
    print getVersion()
