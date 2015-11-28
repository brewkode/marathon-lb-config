class MarathonTaskInfo:
	def __init__(self, host, ports):
		self.host = host
		self.ports = ports

	def http_uri(self):
		return "http://"+self.host+":"+str(self.ports[0])

	def name(self):
		return self.host+":"+str(self.ports[0])
