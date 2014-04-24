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

		data = urllib2.urlopen('http://finance.yahoo.com/d/quotes.csv?s=' + quote(args) + "&f=snd1|l1k2").read()
		data = data.split(",")
		if data[2][1:-1] == 'N/A':
			receiver.msg('Symbol not found, try again.')
			return
		
		price = data[4]
		change = data[-1].split()[2][:-1]

		receiver.msg(chr(2) + args + chr(15) + ': $' + price + " - Today's change " + change)
