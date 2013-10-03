#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2
from urllib import quote
import xml.etree.ElementTree as ET

class BotModule(object):
	def __init__(self, storage):
		self.storage = storage
		self.admins = {}
		self.bot = None
	def register(self):
		return {'functions': [{'stock': self.cmd_stock}], 'aliases': {'stocks': 'stock'}}

	def cmd_stock(self, args, receiver, sender):
		"""stock [symbol] | {'public': True, 'admin_only': False} | Fetches stock value and change"""
		if args == '':
			receiver.msg('Give me a symbol to fetch data for')
			return

		data = urllib2.urlopen('http://www.google.com/ig/api?stock=' + quote(args)).read()
		root = ET.fromstring(data)

		if len(root[0]) <= 4:
			receiver.msg('Symbol not found, try again.')
			return

		change = root[0][18].get('data')
		try:
			if float(change) >= 0:
				change = chr(3) + '03' + root[0][18].get('data') + chr(15)
			else:
				change = chr(3) + '05' + root[0][18].get('data') + chr(15)
		except:
			pass

		receiver.msg(chr(2) + root[0][3].get('data') + chr(15) + ' ' + root[0][10].get('data') + ' ' + root[0][9].get('data') + ' (' + change + ' '+ root[0][21].get('data') +')')