#!/usr/bin/env python
# -*- coding: utf-8 -*-

class BotModule(object):
	def __init__(self, storage):
		self.storage = storage
		self.admins = {}
		self.bot = None
	def register(self):
		return {'functions': [{'xmas': self.cmd_xmas}], 'modifiers': [{'xmasmod': self.mod_xmas}]}

	def cmd_xmas(self, args, receiver, sender):
		"""xmas [on/off] | {'public': False, 'admin_only': True} | Enables or disables christmas mode"""
		args = args.split(' ')[0].lower()
		if args in ['on', 'off']:
			self.storage['xmas'] = args
			receiver.msg('xmas now ' + chr(2) + args)

	def mod_xmas(self, content):
		if content['name'] == 'msg':
			if self.storage['xmas'] == 'on':
				colors = [3, 4]
				out = ''
				i = 0
				for letter in content['message']:
					out += chr(3) + ('0' if colors[i] < 10 else '') + str(colors[i])
					out += letter
					i += 1
					if i >= len(colors):
						i = 0
				content['message'] = out
		return content