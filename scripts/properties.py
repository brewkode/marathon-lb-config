#!/usr/bin/python
import os
import os.path


class Properties(object):
	@classmethod
	def load(klass, cfg_file):
		config = {}
		if not os.path.exists(cfg_file):
			return config

		with open(cfg_file, 'r') as fd:
			for line in fd:
				if line.startswith("#") or len(line.split("=")) != 2:
					continue
				parts = line.strip().split("=")
				config[parts[0]] = parts[1].split("#")[0]
		return config