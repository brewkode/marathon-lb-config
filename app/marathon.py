import socket

class MarathonTaskInfo:
	def __init__(self, host, ports):
		self.host = host
		self.ports = ports
		self.ipaddr = socket.gethostbyname(self.host)

	def http_uri(self):
		return "http://"+self.host+":"+str(self.ports[0])

	def name(self):
		return self.host+":"+str(self.ports[0])

	def resolved_name(self):
		return self.ipaddr+":"+str(self.ports[0])
