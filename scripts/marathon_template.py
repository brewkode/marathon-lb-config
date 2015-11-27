#!/usr/bin/python

import argparse
import urllib2
import json

def http_fetch(url):
	print "Fetching from %s " % url
	req = urllib2.Request(url)
	response = urllib2.urlopen(req)
	return json.loads(response.read())

def fetch_app_ids(marathon_uri):
	apps_json = http_fetch(marathon_uri+"/v2/apps")
	apps = apps_json["apps"]
	app_ids = map(lambda app: app["id"].strip("/"), apps)
	return app_ids

def fetch_tasks(marathon_uri, app_id):
	app = http_fetch(marathon_uri+"/v2/apps/"+app_id)
	app_tasks = app["app"]["tasks"]
	# assuming our apps expose only one port of interest
	tasks = map(lambda task: task["host"]+":"+str(task["ports"][0]), app_tasks)
	response = {}
	response[app_id] = tasks
	return response


if __name__ == '__main__':
	argumentParser = argparse.ArgumentParser(prog='marathon_template', description='Script that\'s used to generate ha_proxy config file from marathon')
	argumentParser.add_argument('-m', '--marathon', help='Marathon URI', required=True)
	argumentParser.add_argument('-a', '--app_name', help='App name for which haproxy config needs to be generated', required=False, default='all')

	args = argumentParser.parse_args()

	print fetch_tasks(args.marathon, args.app_name)