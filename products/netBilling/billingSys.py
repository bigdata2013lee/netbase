#coding=utf-8
import time
import calendar

from products.netPublicModel.userControl import UserControl
from products.netBilling.Billing import Billing
from products.netModel.device import Device
from products.netModel.shortcutCmd import ShortcutCmd
from products.netModel.website import Website
from products.netBilling.billingRecord import BillingRecord
from products.netModel.user.user import User
import datetime

def lastDays():
    "本月共几天？ 离本月最后一天还差几天？"
    c = calendar.Calendar()
    year =  time.localtime().tm_year
    month = time.localtime().tm_mon
    day = time.localtime().tm_mday
    maxDay = max([x[0] for x in c.itermonthdays2(year, month)])
    _lastDays =   maxDay - day
    return maxDay, _lastDays

def _getDayPrice(uPrice):
    "非整月扣费的价格"
    xs=lastDays()
    uPrice=round(xs[1]/float(xs[0]) * uPrice, 2)
    return uPrice
           
        
def _getCompanyCondition(user):
    if user: ownCompany = user.ownCompany
    if ownCompany:
        ownCompanyRefInfo = ownCompany._getRefInfo()
    
    return {"ownCompany":ownCompanyRefInfo}

#------------------------------------------------------------------------------                                  
class BillingSys(object):
    

    """
    注意给主机、站点、开机扣费时，因为已经增加了再扣费的，
    所以已经存在的对象数额包括了新增的对象
    """
    
   
    @staticmethod
    def hasEnoughPolicyForAdd(motype,changeCounts=0):
        """
        @param motype: 类类型，如Device、Network、Process......
        查看用户的计费策略是否有权限添加设备 
        """
        user = UserControl.getUser()
        lp = user.levelPolicy
        conditions = {}
        conditions.update(_getCompanyCondition(user))
        existCount = motype._countObjects(conditions)
        
        moCountName = str(motype.__name__)[0].lower() +str(motype.__name__)[1:]+ "Count"
        moCount = getattr(lp, moCountName, 0)
        if moCount > existCount: return False
        return True
        
#----------------------------------------------------------------------------------------#
        

    @staticmethod
    def hasEnoughMoneyForSMS(user=None):
        """
                判断是否有足够的钱发送短信
        """
        billing = Billing()
        if not user: user = UserControl.getUser()
        if user.money < billing.unitPriceForSMS:return False
        return True
    
    @staticmethod
    def spendForSMS(user=None):
        """
                短信扣费
        """
        if not user: user = UserControl.getUser()
        def priceFun(conditions, billing, xs):
            price = round(xs[1]/float(xs[0]) * billing.unitPriceForSMS, 2)
            print "play %s for send sms." %price
            return price
        bs = _spendFor(priceFun,user=user,itemName="发送一条短信")
        return bs
    
if __name__ == "__main__":
     user = User._loadObj("53732ee3e92c861e208f2e70")
     print user