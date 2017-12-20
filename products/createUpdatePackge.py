#coding=utf-8
import os

import commands
import datetime

appHome = r'/opt/netbase4'
saveDir = r'/root/updatePackges'
#----------------------------------------------------------#
updateCmd = """
cp -uvpr `pwd`/netbase4/*  /opt/netbase4/
"""
packName = 'update_%s' % datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

 
updateFiles = [
"./products/netMinWeb/media/css/base.css",
"./products/netMinWeb/media/images/wj_logo.png",
"./products/netMinWeb/media/images/yx_logo.png",
]

readmeText = """
hello....

"""
#----------------------------------------------------------#
def initSomethings():
    info = commands.getoutput(r'rm -rvf %s/netbase4/' % saveDir)
    info = commands.getoutput(r'mkdir -p %s/netbase4' % saveDir)


def copy2temdir():
    os.chdir(appHome)
    for fpath in updateFiles:
        targetPath = r'%s/netbase4/%s' % (saveDir, fpath)
        targetdir = os.path.dirname(targetPath)
        info = commands.getoutput(r'mkdir -pv %s' % targetdir)
        info = commands.getoutput(r'cp -fv %s  %s/netbase4/%s' % (fpath, saveDir, fpath))
    

def createOthers():
    os.chdir(saveDir)
    readmeFile = open(saveDir + '/readme.txt', 'w+')
    readmeFile.write(readmeText)
    
    text = """
    \n\n\n\n-------------------------files--------------------------------------
    \n"""
    readmeFile.write(text)
    
    for fpath in updateFiles:
        readmeFile.write(fpath)
        
    readmeFile.close()
    
    updateCmdFile = open(saveDir + '/update_cmd.sh', 'w+')
    updateCmdFile.write(updateCmd)
    updateCmdFile.close()
    
    
    
def removeOthers():
    os.chdir(saveDir)
      
def createTarGz():
    os.chdir(saveDir)

    info = commands.getoutput(r'tar -zcvf %s.tar.gz netbase4 readme.txt update_cmd.sh' % packName)



if __name__ == '__main__':
    initSomethings()
    copy2temdir()
    createOthers()
    createTarGz()
    removeOthers()
    
    
    
    
    
