#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2
from bs4 import BeautifulSoup

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
		html = urllib2.urlopen("http://www.coe.neu.edu/cgi-bin/fortune")
		soup = BeautifulSoup(html.read())
		fortune = soup.pre.get_text()
		fortune = fortune.replace("\n", "")
		self.bot.msg(receiver.name, sender.nick + "~ " + fortune)

	def http(self, path, handler):
		return {'title': 'Example web page', 'content': '<p class="lead">This is a cute example page :3</p><p>It looks like you are on the page ' + path + '..</p>'}
