#!/usr/bin/python
#coding=utf-8
from pychartdir import *
from products.netUtils.xutils import nbPath as _p
class ReportGraph(object):
    """
        报表图像生成类
    """
    def __init__(self,dateString):
        """
                分割日期
        """
        self.dateString=dateString
        
    def setXFontAngle(self,labels,c):
        """
                设置X轴字体格式和标题
        """
        c.xAxis().setLabels(labels)
        c.xAxis().setTickOffset(0.5)
        c.xAxis().setLabelStyle("simsun.ttc", 9).setFontAngle(45)
        c.xAxis().setWidth(2)
    
    def setYFontAngle(self,utitle,c):
        """
                设置Y轴字体格式和标题
        """
        c.yAxis().setTickDensity(30)
        c.yAxis().setLabelStyle("simsun.ttc",10)
        c.yAxis().setWidth(2)
        c.yAxis().setTitle(utitle,"simsun.ttc",10)
    
    def createLineGraph(self,datas,labels,devs,gtitle,utitle,colors):
        """
                线性图生成函数
        datas:图上显示的数据,列表格式[[],[],[]]
        labels:时间标签,在X
        devs:设备列表
        gtitle:图的主标题
        utitle:单位名称
        return:二进制的图片格式字符串
        """
        colors=colors*2
        icon=[CircleSymbol,DiamondSymbol,SquareSymbol,TriangleSymbol,Cross2Shape()]
        icon=icon*2
        c = XYChart(760, 330)
        c.setPlotArea(50, 55, 520, 220, c.linearGradientColor(0, 55, 0, 335, 0xf9fcff,
            0xaaccff), -1, Transparent, 0xffffff)
        c.addTitle(gtitle,"simsun.ttc", 12).setPos(0,10)
        c.addLegend(570, 100, 0, "simsun.ttc", 10).setBackground(Transparent)
        self.setXFontAngle(labels, c)
        self.setYFontAngle(utitle, c)
        layer = c.addLineLayer2()
        layer.setLineWidth(2)
        for i in xrange(len(devs)):
            layer.addDataSet(datas[i],colors[i],devs[i]).setDataSymbol(icon[i],6)
        return  c.makeChart2(PNG)
    
    def createMultipleBarChartGraph(self,datas,devs,labels,gtitle,utitle,colors):
        """
                多个柱状图生成函数
        datas:图上显示的数据,列表格式[[],[],[]]
        labels:图像标签,在X
        devs:设备列表
        gtitle:图的主标题
        utitle:单位名称
        return:二进制的图片格式字符串
        """
        c = XYChart(520, 380)
        c.setPlotArea(65, 60, 450, 220)
        c.addTitle(gtitle, "simsun.ttc", 12).setPos(20,10)
        c.addLegend(160, 25, 0, "simsun.ttc", 10).setBackground(Transparent)
        self.setXFontAngle(devs, c)
        self.setYFontAngle(utitle, c)
        layer = c.addBarLayer2(Side, 4)
        for i in xrange(len(labels)):
            layer.addDataSet(datas[i], colors[i], labels[i])
        layer.setBorderColor(Transparent, barLighting(0.75, 1.75))
        layer.setBarGap(0.2, TouchBar)
        layer.setBarWidth(30)
        return c.makeChart2(PNG)
    
    def createPieChartGraph(self,datas,labels,gtitle,colors):
        """
                饼图生成函数
        datas:图上显示的数据,列表格式[[],[],[]]
        labels:图像标签,在X
        devs:设备列表
        gtitle:图的主标题
        utitle:单位名称
        return:二进制的图片格式字符串
        """
        c = PieChart(220, 220)
        c.setPieSize(110, 110, 60)
        c.addTitle(gtitle,"simsun.ttc",10)
        c.set3D()
        c.setData(datas, labels)
        c.setColors2(DataColor, colors)
        c.setLabelStyle("simsun.ttc",10)
        c.setSectorStyle(LocalGradientShading, 0xbb000000,1)
        return c.makeChart2(PNG)
    
    def makeGraphPng(self,graphData,filePath):
        """
                测试生成的图像
        graphData:图像二进制数据
        filePath:图像生成路径
        """
        f=open(filePath,"w")
        f.write(graphData)
        f.close()
        
    def getDataUnit(self,datas):
        """
                报表数据单位转换
        """
        unit="个"
        powers = {"k":1000,"M":1000**2,"G":1000**3}
        maxValue=max([max(i) for i in datas])
        if maxValue<1000:return datas,unit
        for key,value in powers.iteritems():
            maxValue = maxValue / 1000.0
            if maxValue < 1000:
                unit="%s" % (key)
                break
        datas=[map(lambda x:round(x/powers.get(unit,1),2),i)for i in datas]
        return datas,unit

    def getGraphFilePath(self,pri):
        """
                得到图像的文件路径
        """
        import time
        import os
        path=_p("/nbfiles/imgs/reportImgs/")
        if not os.path.exists(path):
            os.system("mkdir %s"%(path))
        graphFilePath="%s%s-%s.PNG"%(path,pri,str(int(time.time())))
        return graphFilePath
    
    def makeEscountGraph(self,escount):
        """
                按事件级别统计事件发生次数图像生成
        """
        pieData=[]
        labels=["Critical","Error","Warn"]
        colors = [0xff0000,0xff9900, 0xffff00]
        #生成图像文件的路径
        escountMultipleBarFilePath=self.getGraphFilePath("escountMultipleBarFilePath")
        escountPieFilePath=self.getGraphFilePath("escountPieFilePath")
        #获取生成图像文件的数据
        deviceName=[i.get("title") for i in escount]
        critical=[i.get(5) for i in escount]
        error=[i.get(4) for i in escount]
        warn=[i.get(3) for i in escount]
        #生成柱状图
        escountMultipleBarData=self.createMultipleBarChartGraph([critical,error,warn],deviceName,labels,"事件统计排行","事件",colors)
        self.makeGraphPng(escountMultipleBarData,escountMultipleBarFilePath)
        #生成饼图
        if  escount:pieData=[sum(critical),sum(error),sum(warn)]
        escountPieData=self.createPieChartGraph(pieData,labels,"",colors)
        self.makeGraphPng(escountPieData,escountPieFilePath)
        
        return escountMultipleBarFilePath,escountPieFilePath
    
    
    def makeCPUTrendGraph(self,cpuTrendValue,graphName,fileName):
        """
        CPU趋势报表图像生成
        """
        colors=[0xff0000,0x00ff00,0xffff00,0xff7f00,0x66ccff,0x6666ff,0x666600,0x0000ff,0x00ffff,0x42426f]
        cpuTrendLineFilePath=self.getGraphFilePath(fileName)
        objNames=cpuTrendValue.keys()
        datas=[cpuTrendValue.get(i) for i in objNames]
        cpuTrendLineData=self.createLineGraph(datas, self.dateString, objNames, graphName, "利用率(%)", colors)
        self.makeGraphPng(cpuTrendLineData,cpuTrendLineFilePath)
        return cpuTrendLineFilePath
        
    def makeMemTrendGraph(self,memTrendValue,graphName,fileName):
        """
        Mem趋势报表图像生成
        """
        colors=[0xff0000,0x00ff00,0xffff00,0xff7f00,0x66ccff,0x6666ff,0x666600,0x0000ff,0x00ffff,0x42426f]
        memTrendLineFilePath=self.getGraphFilePath(fileName)
        objNames=memTrendValue.keys()
        datas=[memTrendValue.get(i) for i in objNames]
        memTrendLineData=self.createLineGraph(datas, self.dateString, objNames, graphName, "利用率(%)", colors)
        self.makeGraphPng(memTrendLineData,memTrendLineFilePath)
        return memTrendLineFilePath
    
    def makeResTimeTrendGraph(self,resTimeTrendValue,graphName,fileName):
        """
                站点响应时间趋势报表图像生成
        """
        colors=[0xff0000,0x00ff00,0xffff00,0xff7f00,0x66ccff,0x6666ff,0x666600,0x0000ff,0x00ffff,0x42426f]
        resTimeTrendLineFilePath=self.getGraphFilePath(fileName)
        objNames=resTimeTrendValue.keys()
        datas=[resTimeTrendValue.get(i) for i in objNames]
        resTimeTrendLineData=self.createLineGraph(datas, self.dateString, objNames, graphName, "毫秒", colors)
        self.makeGraphPng(resTimeTrendLineData,resTimeTrendLineFilePath)
        return resTimeTrendLineFilePath
    
    def makeConnTrendGraph(self,connTrendValue,graphName,fileName):
        """
                连接数趋势报表图像生成
        """
        colors=[0xff0000,0x00ff00,0xffff00,0xff7f00,0x66ccff,0x6666ff,0x666600,0x0000ff,0x00ffff,0x42426f]
        connTrendLineFilePath=self.getGraphFilePath(fileName)
        objNames=connTrendValue.keys()
        datas=[connTrendValue.get(i) for i in objNames]
        connTrendLineData=self.createLineGraph(datas, self.dateString, objNames,graphName, "个数", colors)
        self.makeGraphPng(connTrendLineData,connTrendLineFilePath)
        return connTrendLineFilePath
    
    def makeNewConnTrendGraph(self,newConnTrendValue,graphName,fileName):
        """
                新建连接数趋势报表图像生成
        """
        colors=[0xff0000,0x00ff00,0xffff00,0xff7f00,0x66ccff,0x6666ff,0x666600,0x0000ff,0x00ffff,0x42426f]
        newConnTrendLineFilePath=self.getGraphFilePath(fileName)
        objNames=newConnTrendValue.keys()
        datas=[newConnTrendValue.get(i) for i in objNames]
        newConnTrendLineData=self.createLineGraph(datas,self.dateString,objNames,graphName,"个数", colors)
        self.makeGraphPng(newConnTrendLineData,newConnTrendLineFilePath)
        return newConnTrendLineFilePath
    
    def makeAvilTrendGraph(self,avilTrendValue,graphName,fileName):
        """
                可用性趋势报表图像生成
        """
        colors=[0xff0000,0x00ff00,0xffff00,0xff7f00,0x66ccff,0x6666ff,0x666600,0x0000ff,0x00ffff,0x42426f]
        avilTrendLineFilePath=self.getGraphFilePath(fileName)
        objNames=avilTrendValue.keys()
        datas=[avilTrendValue.get(i) for i in objNames]
        avilTrendLineData=self.createLineGraph(datas,self.dateString,objNames,graphName,"百分比(%)", colors)
        self.makeGraphPng(avilTrendLineData,avilTrendLineFilePath)
        return avilTrendLineFilePath
    
if __name__=="__main__":
    from products.netReport.reportGraph import ReportGraph
    rg=ReportGraph()
    devs=["192.168.11.2","192.168.11.6", "SQL Server"]
    datas=[ [42, 49,62],[89,82, 19]]
    #labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct","Nov", "Dec"]
    #labels=["严重","错误","警告"]
    labels=["snmp","ping"]
    gtitle="设备事件统计排行"
    utitle="事件"
    graphData=rg.createFontChartGraph(datas,labels,devs,gtitle,utitle)
    rg.testGraph(graphData)
