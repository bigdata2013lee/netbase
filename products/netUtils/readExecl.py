#coding=utf-8
import os
import xlrd

class ReadExecl(object):
    """
    execl读取类
    """
    def __init__(self,fileName,byName):
        """
                初始化函数
        """
        self.fileName=fileName
        self.byName=byName
        
    def openExcel(self):
        """
                读取excel
        """
        try:
            data = xlrd.open_workbook(self.fileName)
            return data
        except Exception,e:
            print str(e)
            
    def rowstrip(self,row):
        """
                去空格
        """
        row=[i.strip() for i in row]
        return row

    def excelTableByName(self,colnameindex=1):
        """
                根据名称获取Excel表格中的数据
        fileName:Excel文件路径     
        colnameindex:头列名所在行
        byName:名称
        """
        data = self.openExcel()
        table = data.sheet_by_name(self.byName)
        nrows = table.nrows #行数 
        listData =[]
        for rownum in xrange(1,nrows):
            row = table.row_values(rownum)
            if row:
                listData.append(row)
        return listData
    
    def parseExcel(self):
        """
                解析excel数据
        fileName:excel文件路径
        """
        try:
            tables = self.excelTableByName()
            if tables is not None:
                return tables
            else:
                print "excel中数据为空!"
        except:
            return None