#!/usr/bin/python
#coding=utf-8
import os
from pychartdir import *
from products.netUtils.xutils import nbPath as _p
class DistributionGraph(object):
    """
    报表图像生成类
    """
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
        c.xAxis().setLabels(devs)
        c.xAxis().setTickOffset(0.5)
        c.xAxis().setLabelStyle("simsun.ttc", 10).setFontAngle(30)
        c.yAxis().setLabelStyle("simsun.ttc", 10)
        c.xAxis().setWidth(2)
        c.yAxis().setWidth(2)
        c.yAxis().setTitle(utitle,"simsun.ttc",10)
        #字体具体y轴的距离
        #c.yAxis().setLabelGap(0)
        #c.yAxis().setMinTickInc(5)
        layer = c.addBarLayer2(Side, 4)
        for i in xrange(len(labels)):
            layer.addDataSet(datas[i], colors[i], labels[i])
        layer.setBorderColor(Transparent, barLighting(0.75, 1.75))
        layer.setBarGap(0.2, TouchBar)
        layer.setBarWidth(30)
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

    def getGraphFilePath(self,pri):
        """
        得到图像的文件路径
        """
        import time
        path=_p("/nbfiles/imgs/")
        if not os.path.exists(path):
            os.system("mkdir %s"%(path))
        graphFilePath="%s%s%s.PNG"%(path,pri,time.time())
        return graphFilePath
    
    def makeWebSiteDistributionGraph(self,distributionDatas):
        """
        站点的延时可用性分布图
        """
        webSiteName=[]
        datas=[[],[],[]]
        for key,value in distributionDatas.iteritems():
            webSiteName.append(key)
            datas[2].append(value[0])
            datas[1].append(value[1])
            datas[0].append(value[2])
        labels=["正常","延时","不可用"]
        colors = [0x008000,0xff9900,0xff0000]
        #生成图像文件的路径
        webSiteDistributionFilePath=self.getGraphFilePath("webSiteDistributionFilePath")
        #生成柱状图
        webSiteDistributionData=self.createMultipleBarChartGraph(datas,webSiteName,labels,"站点综合评估排行","百分比",colors)
        self.makeGraphPng(webSiteDistributionData,webSiteDistributionFilePath)
        return webSiteDistributionFilePath.split("/")[-1]
    
    def makeMiddlewareDistributionGraph(self,distributionDatas):
        """
        中间件的延时可用性分布图
        """
        middlewareName=[]
        datas=[[],[],[]]
        for key,value in distributionDatas.iteritems():
            middlewareName.append(key)
            datas[2].append(value[0])
            datas[1].append(value[1])
            datas[0].append(value[2])
        labels=["正常","延时","不可用"]
        colors = [0x008000,0xff9900,0xff0000]
        #生成图像文件的路径
        middlewareDistributionFilePath=self.getGraphFilePath("middlewareDistributionFilePath")
        #生成柱状图
        middlewareDistributionData=self.createMultipleBarChartGraph(datas,middlewareName,labels,"中间件综合评估排行","百分比",colors)
        self.makeGraphPng(middlewareDistributionData,middlewareDistributionFilePath)
        return middlewareDistributionFilePath.split("/")[-1]

