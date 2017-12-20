#coding=utf-8
import re
from products.netCommand.commandParser import CommandParser
pattern = re.compile(r"Server:(.+)\r")
class iisParser(CommandParser):
  
    def processResults(self, cmd, result):

        output = cmd.result.output
        version = re.findall(pattern,output)[0]
       
        for dp in cmd.points:
            if dp.dpname == "mwVersion":
                result.values.append( (dp, version) )
  
        return result


