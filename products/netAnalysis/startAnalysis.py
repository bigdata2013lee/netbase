#coding=utf-8


from analysis import Analysis
from products.netRealTimeDB.redisClient import Client
from products.netUtils.settings import CollectorSettings
import time



    



if __name__ == '__main__':
    
    client = Client(host=CollectorSettings.getSettings().get("redis","redisHost"), port=CollectorSettings.getSettings().getAsInt("redis","redisPort"))
    ana = Analysis()
    ana.setDBClient(client)
    ana.work()
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        exit()
    
    
    
    
