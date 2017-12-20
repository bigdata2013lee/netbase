#coding=utf-8

import time
from products.netPublicModel.modelManager import ModelManager
from products.netTasks import NetbaseSysTask
from products.netUtils import xutils


style="""
<style>
#grid_table1{
    border-collapse: collapse;
    font-size:12px;
    font-family: arial;
    color:#333;
    border:1px solid #C1D9F3;
    width:800px;
}

#grid_table1 thead{
 background-color:#EFF5FB;
}
#grid_table1 td{padding:4px;border-bottom:1px solid #C1D9F3;}

#grid_table1 span.severity3{color:#FF9D3C}
#grid_table1 span.severity4{color:#FF5353}
#grid_table1 span.severity5{color:#CA0000}


p.fotter{
margin-top:4em;
font-size:12px;
font-family: arial;
color:#005BB7;
background-color:#f5f5f5;
padding:1em;
}

p{
font-size:12px;
font-family: arial;
}
</style>

"""

p1Html = """
<p>
<img src="http://www.wanjee.cn/media/help/login_logo.png"/><br/>
网脊运维通系统为您报告最新事件消息，以下是相关信息：
</p>
"""

p2Html = """
<p>
此外，您还可以登陆www.wanjee.cn,获取更多的事件警告信息。
</p>
"""

p3Html = """
<p class="fotter">
此邮件是由网脊运维通系统发出，系统不接收回信，请勿直接回复<br/><br/>
如果您有任何疑问或建议，请加入我们的Q群共同探讨<br/>
华南交流群:37960299<br/>
华东交流群:315888922<br/>
华北交流群:328557644<br/><br/>

或致电联系我们400-6352-500
</p>
"""

tableHtml = """
<table id="grid_table1">
    <thead>
        <tr>
        <td>级别</td>
        <td>名称</td>
        <td>监控项目</td>
        <td>事件消息</td>
        <td>结束时间</td>
        <tr>
    </thead>
    <tbody>
    %s
    </tbody>
</table>
"""

trHtml="""
<tr>
    <td>%s</td>
    <td>%s</td>
    <td>%s</td>
    <td>%s</td>
    <td>%s</td>
</tr>
"""

severitys={"0":"清除", "1":"debug", "调试":"info", "3":"警告", "4":"错误", "5":"严重"}
componentTypes={
                "IpService":"IP服务", "Process":"进程", "IpInterface":"接口", "FileSystem":"文件系统",
                "Device":"设备", "Network":"网络",
                "MwApache":"Apache","MwTomcat":"Tomcat", "MwNginx":"Nginx",
    }
def findEvents(user):
    evtMgr = ModelManager.getMod('eventManager')
    #from products.netEvent.eventManager import EventManager
    #evtMgr = EventManager()
    if not user: return []
    if not user.ownCompany: return []
    
    conditions = {
        "companyUid": user.ownCompany.getUid()
    }
    
    events = evtMgr.findCurrentEvents(conditions=conditions, sortInfo={"endTime":-1}, limit=50)
    return events

def  createEventsTable(events):
    trs=[]
    for evt in events:
        x1 =  '<span class="severity%s">%s</span>' %(evt.severity, severitys.get( "%s" %evt.severity, ""))
        x2 = evt.label
        x3 = componentTypes.get(evt.componentType, evt.componentType)
        x4 = evt.message
        x5 = xutils.formartTime(evt.endTime, fm="%Y-%m-%d %H:%M")
        
        tr = trHtml %(x1, x2, x3, x4, x5)
        trs.append(tr)
        
    return tableHtml % "".join(trs)

def sendEmailToUser(user):
    events = findEvents(user)
    if not events: return 
    table = createEventsTable(events)
    subject = "网脊运维通事件日报"
    recipient_list=[user.email]
    message = style+p1Html + table + p2Html + p3Html
    xutils.sendMail(subject, style+message, recipient_list, attachments=[])
    return


def sendEventEmailReport():
    "为所有的用户发送每日事件报告"
    from products.netModel.user.user import User
    users = User._findObjects()
    for u in users:
        try:
            sendEmailToUser(u)
        except Exception,e:
            print e
        
class Task(NetbaseSysTask):
    
    def __runService__(self):
        
        while True:
            time.sleep(10)
            timeXstr =  "%s:%s" % time.localtime()[3:5]
            if timeXstr != "20:0": continue #定时晚上20:00
            sendEventEmailReport()
            time.sleep(3600)
        


        

