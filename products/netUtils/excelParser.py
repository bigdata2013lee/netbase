#coding=utf-8
import re
import  xlrd
from products.netModel.user.user import User


class ExcelError(Exception):
    pass

    
def STR(x):
    try:r = str(int(x))
    except:return x
    else:return r  
    
def checkInfo(userInfo,line):
    """验证用户信息是否合法"""
    if 2 <= len(userInfo["company"]) <= 20:pass
    else:raise ExcelError(u"第%d行:%s不是一个有效的公司名称 "  %(line,userInfo["company"]))
            
    p_email = re.compile("^[\w\d]+[\d\w\_\.]+@([\d\w]+)\.([\d\w]+)(?:\.[\d\w]+)?$")
    if re.match(p_email,userInfo["email"]):pass
    else:raise ExcelError(u"第%d行:%s不是一个有效的邮箱 "  %(line,userInfo["email"]))
            
    p_mphone = re.compile("1\d{10}$")
    p_sphone = re.compile("(0\d{2,3})-\d{7,8}$") 
    userInfo["contactPhone"] = STR(userInfo["contactPhone"])
    if re.match(p_mphone,userInfo["contactPhone"]) or re.match(p_sphone,userInfo["contactPhone"]):pass
    else:raise ExcelError(u"第%d行:%s不是一个有效的联系电话 "  %(line,userInfo["contactPhone"]))
    
    return True

def checkEmail(userInfos):
    """验证用户信息中email是否重复；email是否已经注册过"""
    emails = []
    for userInfo in userInfos:
        emails.append(userInfo["email"])
    if len(emails) > len(set(emails)):
        raise ExcelError(u"上传的文件中存在相同的邮箱，但是同一个邮箱只能注册一个帐号")
    for email in emails:
        condition = {"email":email}
        if User._findObjects(condition):
            raise ExcelError(u"邮箱 %s已经注册过帐号，不能重复注册" %email)
    return True
    
    
def excelParser(filename):
    userInfos = []
    try:
        data = xlrd.open_workbook(filename)
    except Exception:
        raise ExcelError(u"上传的文件格式不正确，请确认后再上传")
    
    if data:tables = data.sheets()
    else:return 
    for table in tables:
        nrows = table.nrows
        if nrows < 2 :break
        ncols = table.ncols
        if ncols != 3:break       
        labels = table.row_values(0)
        informLabels = ['','','']  
        for i in xrange(len(labels)):
            if labels[i].find(u"公司")>-1:informLabels[i] = "company"        
            elif labels[i].find(u"邮箱")>-1:informLabels[i] = "email"
            elif labels[i].find(u"电话")>-1:informLabels[i] = "contactPhone" 
            else:break         
        if '' in informLabels:break 
        for r in xrange(1,nrows):
            inform = table.row_values(r)
            userInfo = dict(zip(informLabels,inform)) 
            line = r+1
            if checkInfo(userInfo,line):
                userInfos.append(userInfo)
    if checkEmail(userInfos):
        return userInfos
         
   
if __name__=="__main__":
    f="/opt/e.xls"
    print excelParser(f)
       
    