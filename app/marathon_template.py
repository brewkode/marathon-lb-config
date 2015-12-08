#!/usr/bin/python

import argparse
import urllib2
import json
from jinja2 import Environment, Template, FileSystemLoader

from app.properties import Properties
from app.marathon import MarathonTaskInfo

class MarathonTemplate(object):
  def __init__(self, marathon):
    self.marathon_client = marathon

  def render(self, template, out_file, variables):
    env = Environment(loader=FileSystemLoader('templates'))
    svc_name = template.split(".")[0]
    properties = Properties.load("conf/"+svc_name+".properties")

    template = env.get_template(template)
    rendered_template = template.stream(j2 = variables, props = {svc_name : properties})
    rendered_template.dump(out_file)

  def fetch_tasks(app_id):
    def is_alive(task):
      return len(task.health_check_results) > 0 && task.health_check_results[0].alive
      
    app_tasks = [ task for task in marathon.list_tasks(app_id) if is_alive(task) ]
    tasks = map(lambda task: MarathonTaskInfo(task.host, task.ports), app_tasks)
    return tasks

  def tasks_for(marathon_url, apps):
    response = {}
    for app in apps:
      try:
        response[app] = self.fetch_tasks(marathon_url, app)
      except:
        print "Failed fetching task info for %s" % (app)
    return response

if __name__ == '__main__':
  def to_set(param, sep=','):
    return set(param.split(sep))

  argumentParser = argparse.ArgumentParser(prog='marathon_template', 
    description='Script that\'s used to generate ha_proxy config file from marathon')
  argumentParser.add_argument('-m', '--marathon', help='Marathon URI', required=True)
  argumentParser.add_argument('-a', '--app_name', type=to_set, help='App name for which haproxy config needs to be generated', required=True)
  argumentParser.add_argument('-t', '--template_file', help='Template file which on which rendering would be done', required=True)
  argumentParser.add_argument('-o', '--out_file', help='Output file', required=True)

  args = argumentParser.parse_args()

  marathon_template = MarathonTemplate()
  response = marathon_template.tasks_for(args.marathon, args.app_name)
  marathon_template.render(args.template_file, args.out_file, response)