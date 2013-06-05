#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ystockquote

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

		_all = ystockquote.get_all(args)
		change = _all['change']
		try:
			if float(_all['change']) >= 0:
				change = chr(3) + '03' + _all['change'] + chr(15)
			else:
				change = chr(3) + '05' + _all['change'] + chr(15)
		except:
			pass

		receiver.msg(chr(2) + args.upper() + chr(15) + ': ' + _all['price'] + ' (' + change + ')')