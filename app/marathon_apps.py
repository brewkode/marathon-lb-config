import socket

class MarathonAppInfo:
	def __init__(self, name, labels, tasks):
		self.name = name
		self.labels = labels
		self.tasks = tasks

	def get_label(self, name, default):
		return self.labels.get(name, default)

	def get_port(self):
		return self.get_label('port')

	def has_portlabel(self):
		return hasattr(self.labels, 'port')

	def should_monitor(self, apps_to_monitor=None):
		if apps_to_monitor is None:
			apps_to_monitor = []
		return (self.has_portlabel() or (self.name in apps_to_monitor))