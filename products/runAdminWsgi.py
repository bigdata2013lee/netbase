import os
import wsgiserver
from django.core.wsgi import WSGIHandler
import sys
import time
from threading import Thread


def startAdmin():
    def target():
        time.sleep(1)
        from products.netPublicModel import startAdminApp
        startAdminApp.startApp()
        
    th = Thread(target=target)
    th.setDaemon(True)
    th.start()
    
if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "netAdminWeb.settings")
    ipAddress = "0.0.0.0"
    port = 8080
    threadsNum = 50
    queueSize = 300
    
    if len(sys.argv)>=2: port = int(sys.argv[1])
    
    wserver = wsgiserver.CherryPyWSGIServer(
    	(ipAddress, port),
    	WSGIHandler(),
    	server_name='netbase_admin',
    	numthreads=threadsNum,
    	request_queue_size=queueSize,
    )
    try:
        startAdmin()
        wserver.start()

    except KeyboardInterrupt:
        wserver.stop()
        sys.exit(2)
    
