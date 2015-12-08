# marathon_handler.py
import falcon
import json
import socket
import argparse
from wsgiref import simple_server

from marathon import MarathonClient, EventFactory


class MarathonEventHandler(object):
	def __init__(self, marathon_client, callback_uri):
		self.update_in_progress = 0
		self.marathon_client = marathon_client
		self.callback_uri = callback_uri
		self.marathon_client.create_event_subscription(self.callback_uri)
		self.marathon_template = MarathonTemplate(self.marathon_client)
		self.event_factory = EventFactory()

	def on_post(self, req, resp):
		payload = req.stream
		for each in payload:
			try:
				event = self.event_factory.process(json.loads(each))
				# Do event processing
			except:
				print "IGNORE_EVENT %s" % each
		resp.body = json.dumps({"status": "ok"})

	# delete subscription on shutdown
	def shutdown(self):
		self.marathon_client.delete_event_subscription(self.callback_uri)


if __name__ == '__main__':
	argumentParser = argparse.ArgumentParser(prog='Marathon template rendering service', 
	description='Service that registers for events on marathon and renders / updates templates based on marathon events')
	argumentParser.add_argument('-m', '--marathon_host', help='Marathon URI', required=True)
	argumentParser.add_argument('-p', '--port', type=int, help='port on which this app should listen', required=True)
	argumentParser.add_argument('-a', '--app_name', type=to_set, help='App name for which template needs to be rendered', required=True)
	argumentParser.add_argument('-t', '--template_file', help='Template file which which would be rendered', required=True)
	argumentParser.add_argument('-o', '--out_file', help='Output file', required=True)
	args = argumentParser.parse_args()

	marathon_host = args.marathon_host
	port = args.port
	app_name = args.app_name
	template_file = args.template_file
	out_file = args.out_file

	event_listener_endpoint = '/marathon/updates'
	callback_uri = "http://"+socket.getfqdn()+":"+str(port)+event_listener_endpoint
	handler = MarathonEventHandler(MarathonClient([marathon_host]), callback_uri)

	api = falcon.API()
	api.add_route(event_listener_endpoint, handler)

    httpd = simple_server.make_server('0.0.0.0', port, api)
    httpd.serve_forever()

    handler.shutdown()
