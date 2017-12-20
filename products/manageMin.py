# -*- coding: utf-8 -*-
from django.core.management import execute_manager
import sys, os
import time
from threading import Thread

try:
    reload(sys)
    sys.path.append(os.getcwd())
    from netMinWeb import  settings # Assumed to be in the same directory.
except ImportError, e:
    print e
    sys.exit(1)




def startNetbase():
    time.sleep(1)
    from products.netPublicModel import startNetbaseApp
    startNetbaseApp.startApp()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.argv.append("runserver")
    try:
        th =  Thread(target=startNetbase)
        th.setDaemon(True)
        th.start()
        
        execute_manager(settings)
    except Exception, e:
        import traceback;traceback.print_exc();
        sys.exit(2)

