#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading
import urllib2
import time
import json

class BotModule(object):
	def __init__(self, storage):
		self.storage = storage
		self.admins = {}
		self.bot = None
		self.kernelURL = 'http://www.kernel.org/releases.json'
		self.interval = 180

		threading.Thread(target=announce, args=(self,)).start()
	def register(self):
		return {'functions': [{'kernelon': self.cmd_enable}, {'kerneloff': self.cmd_disable}], 'aliases': {'k-on': 'kernelon', 'k-off': 'kerneloff'}}
				
	##############
	#Registered command
	##############
	def cmd_enable(self, args, receiver, sender):
		"""kernelon | {'public': True, 'admin_only': False} | Enables announcing new Linux kernels on current channel"""
		tmp = self.storage['kernel']
		if tmp.get('channels') is None:
			tmp['channels'] = [receiver.name]
		else:
			tmp['channels'].append(receiver.name)
		self.storage['kernel'] = tmp
		self.bot.msg(receiver.name, chr(3) + '03[info]' + chr(15) + ' enabled announcing of new Linux kernels on this channel')

	def cmd_disable(self, args, receiver, sender):
		"""kerneloff | {'public': True, 'admin_only': False} | Disables announcing new Linux kernels on current channel"""
		tmp = self.storage['kernel']
		if receiver.name in tmp.get('channels'):
			tmp['channels'].remove(receiver.name)
			self.bot.msg(receiver.name, chr(3) + '08[info]' + chr(15) + ' disabled announcing of new Linux kernels on this channel')
		else:
			self.bot.msg(receiver.name, chr(3) + '04[err]' + chr(15) + ' this channel is not on the announce list')
		self.storage['kernel'] = tmp

def announce(module):
	while True:
		data = json.loads(urllib2.urlopen(module.kernelURL).read())
		if data['releases'][0]['released']['timestamp'] > module.storage['kernel'].get('last', 0):
			tmp = module.storage['kernel']
			tmp['last'] = data['releases'][0]['released']['timestamp']
			module.storage['kernel'] = tmp

			for channel in module.storage['kernel'].get('channels', []):
				module.bot.msg(channel, chr(3) + '02[Linux Kernel]' + chr(15) + ' version ' + \
					chr(2) + data['releases'][0]['version'] + chr(15) + ' now on ' + \
					chr(2) + data['releases'][0]['moniker'] + chr(15) + ', get it on ' + \
					chr(2) + data['releases'][0]['source'] + chr(15))
				time.sleep(1.5)
		time.sleep(module.interval)