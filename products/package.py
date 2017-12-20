# -*- coding: utf-8 -*-
import os
import zipfile
import time
import fnmatch
import threading
import compileall


def famatch(fn, matches):
    for m in matches:
        if fnmatch.fnmatch(fn, m):
            return True
    return False

def zip_dir(source_dir, target_file, match=['*'], exclude_dirs=[], exclude_files=[],other_py_file=[]):
    myZipFile = zipfile.ZipFile(target_file, 'w' )
    for root,dirs,files in os.walk(source_dir):
        for xdir in exclude_dirs:
            if xdir in dirs:
                dirs.remove(xdir)
        if files:
            other_files=filter(lambda f: famatch(f, other_py_file), files)
            src_files=filter(lambda f: famatch(f, match), files)
            files=filter(lambda f: not famatch(f, exclude_files), src_files)
            files=files+other_files
            if os.path.split(root)[1]=="commands" and os.path.split(os.path.split(root)[0])[1]=="management":
                files=files+src_files
                
            for vfileName in files:
                fileName = os.path.join(root,vfileName)
                myZipFile.write( fileName, fileName, zipfile.ZIP_DEFLATED )
    myZipFile.close()

def unzip_file(source_file, target_dir):
    fl={}
    if not os.path.exists(target_dir):
        os.mkdir(target_dir)
    if target_dir[-1] not in ["/","\\"]:
        target_dir+="/"                                    
    z=zipfile.ZipFile(source_file, 'r')
    for fn in z.namelist():
        bytes=z.read(fn)
        filename=target_dir+fn
        if (len(bytes)==0) and (fn[-1] in ["/","\\"]):                     
            try:
                os.makedirs(filename)
            except: pass
        else:
            try:
                os.makedirs("/".join(filename.split('/')[:-1]))
            except: pass
            file(filename,"wb+").write(bytes)
            fl[filename]=len(bytes)
    return fl

def get_tmp_dir(root_path):
    u"""
        临时文件夹路径
    """
    tmp_dir=os.path.join(root_path,"package_tmp")
    try:
        os.makedirs(tmp_dir)
    except: pass
    return tmp_dir

def generate_svn_info(root_path):
    u"""
        得到版本信息
    """
    import pysvn
    client = pysvn.Client()
    info = client.info(root_path)
    try:
        f = file(os.path.join(root_path,"version.log"),"w")
        f.write("%s"%info.data)
    except:
        import traceback
        traceback.print_exc()
    else:
        f.close()


def generate_package(root_path):
    u"""
        生成包
    """
    try:
        generate_svn_info(root_path)
    except:
        import traceback
        traceback.print_exc()
        
    compileall.compile_dir(root_path)
    
    target_file = get_tmp_dir(root_path)+'/mysite.zip'
    match = ['*']
    exclude_dirs = ['docs','package_tmp','nginx','.hg','_svn','.idea','.svn',]
    exclude_files = ['.*','icdat.db','*.swp','*.py','*.orig','*.zip','*.sql', '*.7z', '*.doc',]
    other_include_files = ['settings.py',]
    
    zip_dir(root_path, target_file, match, exclude_dirs,exclude_files ,other_include_files)
#    try:
#        os.removedirs(get_tmp_dir(root_path)+"/mysite")
#    except: pass
#    unzip_file(get_tmp_dir(root_path)+'/mysite.zip', get_tmp_dir(root_path)+"/mysite/")

def generate_release_package(work_path):
    u"""
        生成发布包
    """
    os.chdir(work_path)
    if os.name=='posix':
        os.system('find ./ -iname "*.pyc" -type f|xargs rm -rf')
    else:
        os.system("del *.pyc /s")
    generate_package(work_path)
       
def get_svn_diff_summary(work_path,old_version,new_version):
    u"""
    得到更新文件
    """
    import pysvn
    client = pysvn.Client()
    print 'get updated file information from svn version %s to svn version %s.\n' % (old_version, old_version)

    head = pysvn.Revision(pysvn.opt_revision_kind.number, old_version)
    end = pysvn.Revision(pysvn.opt_revision_kind.number, new_version)


    FILE_CHANGE_INFO = {
        pysvn.diff_summarize_kind.normal: 'normal',
        pysvn.diff_summarize_kind.modified: 'modified',
        pysvn.diff_summarize_kind.delete: 'delete',
        pysvn.diff_summarize_kind.added: 'added',
    }

    upgrade_files_or_dirs = []
    delete_files_or_dirs = []
    summary = client.diff_summarize(work_path, head, work_path, end)
    for info in summary:
        path = info.path
        if info.node_kind == pysvn.node_kind.dir:
            path += '/'
        file_changed = FILE_CHANGE_INFO[info.summarize_kind]
        prop_changed = ' '
        if info.prop_changed:
            prop_changed = "modified"
        absolute_path = os.path.join(work_path,path)
        if file_changed != "delete":
            if os.path.isfile(path):
                file_content = client.cat(absolute_path,end,end)
                upgrade_files_or_dirs.append([file_changed,path,file_content])
        else:
            delete_files_or_dirs.append(path)
        
    return delete_files_or_dirs,upgrade_files_or_dirs


def generate_svn_upgrade_package(svn_root_path,old_version,new_version):
    u"""
    生成更新包
    """
    delete_files , upgrade_files = get_svn_diff_summary(svn_root_path,old_version,new_version)
    
    tmp_dir = get_tmp_dir(svn_root_path)+"/upgrade"
    for change_type,file_path,file_content in upgrade_files:
        absolute_path= os.path.join(tmp_dir,file_path)
        file_dir = os.path.split(absolute_path)[0]
        
        if not os.path.exists(file_dir):
            try:
                os.makedirs(file_dir)
            except:pass
        try:
            f = file(absolute_path,"w")
            f.write(file_content)
        except:
            pass
        else:
            f.close()
    compileall.compile_dir(tmp_dir)
    
    for root,dirs,files in os.walk(tmp_dir):
        if files:
            if os.path.split(root)[1]=="commands" and os.path.split(os.path.split(root)[0])[1]=="management":
                pass
            else:
                for f in files:
                    if f.endswith(".py"):
                        file_path = os.path.join(root,f)
                        try:
                            os.remove(file_path)
                        except:
                            import traceback
                            traceback.print_exc()
                
                
        

if __name__=="__main__":
    root_path = os.getcwd()
    generate_release_package(root_path)
    

