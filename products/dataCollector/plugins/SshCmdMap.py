from products.dataCollector.plugins.CollectorPlugin import CommandPlugin

class SshCmdMap(CommandPlugin):
    
    maptype = "SshCmdMap" 
    command = ''
    def process(self,device,results,log):
        return "",results