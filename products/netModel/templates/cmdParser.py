#coding=utf-8

class CmdParser(object):
	@staticmethod
	def parse(cmd, mo=None):
		if not mo: return cmd
		exec(cmd)
		return cmd

if __name__=="__main__":
	cmd = """cmd="ping "+mo.get("manageIp")"""