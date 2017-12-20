#coding=utf-8
import os
import random
import commands
from products.netUtils.xutils import nbPath as _p
class ExportReport(object):
    """
        报表导出
    """
    baseDir = _p("/nbfiles/imgs/reportImgs/")
    def __init__(self,userid):
        """
                初始化
        """
        self.exportName="%s%s"%(userid,random.randint(1,1000))
        

    def exportReport(self,etype='pdf',htmlContent=''):
        """
                报表导出
        """
        self.createHtml(htmlContent)
        toPath=self.createExportFile(etype)
        return toPath

    def createHtml(self, htmlContent=""):
        """
                创建html
        """
        exportHtmlPath=self.baseDir + '%sexport.html'%self.exportName
        htmlContent = htmlContent.replace("/chart_images/reportImgs",self.baseDir)
        html= """
            <!DOCTYPE html>
            <html>
                <head>
                    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
                </head>
                <body>
                %s
                </body>
            </html>
        """%htmlContent
        ff = open(exportHtmlPath,'w+')
        ff.write(html);
        ff.close()
        
    def createExportFile(self, ftype="pdf"):
        """
                创建输出文件
                生成pdf命令:wkhtmltopdf-amd64
                生成图片命令:wkhtmltoimage-amd64
        """
        wktype=ftype
        if ftype in ["jpg","png"]:wktype="image"
        htmlPath="%s%sexport.html"%(self.baseDir,self.exportName)
        toPath="%s%sexport.%s"%(self.baseDir,self.exportName,ftype)
        cmd = _p(r"/libexec/wkhtmlto%s-amd64 %s %s" %(wktype,htmlPath,toPath))
        commands.getoutput(cmd)
        if not os.path.exists(toPath):return None
        return toPath