#coding=utf-8
from products.netUtils.xutils import importClass
from xml.etree import ElementTree

__doc__ = "仅用来解析由dictToXml生成的xml文件"

def analyTomanycont(xnode):
    dct = {}
    root = xnode.getchildren()
    for node in root:
        if node.tag == "object":
            dct[node.get("id")]={}
        children = node.getchildren()
        for child in children:
            if child.tag == "property":
                dct[node.get("id")][child.get("id")] = child.text
            if child.tag == "tomanycont":
                dct[node.get("id")][child.get("id")] = analyTomanycont(child)
    return dct

def parser(filename):
    medata={}
    tree = ElementTree.parse(filename)
    root=tree.getroot()
    for node in root:
        children = node.getchildren()
        if node.tag == "object":
            medata["_id"]=node.attrib.get("id")
            module = node.attrib.get("module")
            classname = node.attrib.get("class")
        for child in children:
            if child.tag == "property":
                medata[child.get("id")]=child.text
            if child.tag == "tomanycont":
                medata[child.get("id")] = analyTomanycont(child)
    return medata,module,classname
if __name__=="__main__":
    filename = 'new.xml'
    medata,module,classname = parser(filename)
    tpl = importClass(module,classname)()
    print tpl._medata
    tpl._medata = medata
    print tpl._medata
    print tpl















