#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

class BotModule(object):
	def __init__(self, storage):
		self.storage = storage
		self.admins = {}
		self.bot = None
	def register(self):
		return {'functions': [{'fortune': self.fortune_cmd}]}
				
	def fortune_cmd(self, args, receiver, sender):
		"""fortune_cmd | {'public': True, 'admin_only': False} | 
		Retrieves a unix fortune"""
		fortune = os.popen("fortune").readlines()
		self.bot.msg(receiver.name, sender.nick + "~ " + fortune[0])
		if len(fortune) == 1:
			return
		fortune = fortune[1:]
		for line in fortune:
			self.bot.msg(receiver.name, line.strip())

	def http(self, path, handler):
		return {'title': 'Example web page', 'content': '<p class="lead">This is a cute example page :3</p><p>It looks like you are on the page ' + path + '..</p>'}
