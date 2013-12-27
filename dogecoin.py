#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json, urllib2

class BotModule(object):
	def __init__(self, storage):
		self.storage = storage
		self.admins = {}
		self.bot = None
		self.url = 'http://www.cryptocoincharts.info/v2/api/tradingPair/'
	def register(self):
		return {'functions': [{'doge': self.cmd_doge}], 'aliases': {'dgc': 'doge'}}
	def event(self, ev):
		pass

	def cmd_doge(self, args, receiver, sender):
		"""doge | {'public': True, 'admin_only': False} | Gets dogecoin value"""
		ltc = json.loads(urllib2.urlopen(self.url + 'doge_ltc').read())
		btc = json.loads(urllib2.urlopen(self.url + 'doge_btc').read())

		ltc_diff = (float(ltc['price'])/100) * (float(ltc['price'])-float(ltc['price_before_24h']))
		btc_diff = (float(btc['price'])/100) * (float(btc['price'])-float(btc['price_before_24h']))

		ltc_diff_str = str(ltc_diff)[:4 if ltc_diff < 0 else 3]
		btc_diff_str = str(btc_diff)[:4 if btc_diff < 0 else 3]

		ltc_diff_str = chr(3) + ('04' if ltc_diff < 0 else '03') + ltc_diff_str + '%' + chr(15)
		btc_diff_str = chr(3) + ('04' if btc_diff < 0 else '03') + btc_diff_str + '%' + chr(15)

		receiver.msg('1 DOGE is ' + str(ltc['price']) + ' LTC ('+ ltc_diff_str + ') and ' + str(btc['price']) + ' BTC ('+ btc_diff_str + ')')