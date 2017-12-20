import os
import wsgiserver
from django.core.wsgi import WSGIHandler
import time
import sys
from threading import Thread
reload(sys)
sys.setdefaultencoding("utf-8")

def startNetbase():
    def target():
        time.sleep(1)
        from products.netPublicModel import startNetbaseApp
        startNetbaseApp.startApp()
        
    th = Thread(target=target)
    th.setDaemon(True)
    th.start()


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "netMinWeb.settings")
    ipAddress = "0.0.0.0"
    port = 80
    threadsNum = 50
    queueSize = 300
    
    if len(sys.argv)>=2: port = int(sys.argv[1])
    
    wserver = wsgiserver.CherryPyWSGIServer(
    	(ipAddress, port),
    	WSGIHandler(),
    	server_name='netbase',
    	numthreads=threadsNum,
    	request_queue_size=queueSize,
    )
    try:
        startNetbase()
        wserver.start()

    except KeyboardInterrupt:
        wserver.stop()
        sys.exit(2)
