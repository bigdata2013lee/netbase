#coding=utf-8
###########################################################################
#
#
#此软件版权为深圳商之杰科技有限公司所有,更多信息请访问www.netbase.asia
#
#
###########################################################################

import logging
log = logging.getLogger('netcommand')

from pprint import pformat

class ParsedResults:

    def __init__(self):
        self.events = []                # list of event dictionaries
        self.values = []                # list of (DataPointConfig, value)
        
    def __repr__(self):
        args = (pformat(self.events), pformat(self.values))
        return "ParsedResults\n  events: %s\n  values: %s}" % args

class CommandParser:

    def dataForParser(self, context, datapoint):
        return {}

    def processResults(self, cmd, results):
        """
        处理命令行获取的结果
        """
        print 
