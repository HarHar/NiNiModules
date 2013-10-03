#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
	@author: HarHar (https://github.com/HarHar)
	
	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

import socket
import json
import time

class vndbException(Exception):
	pass

class VNDB(object):
	""" Python interface for vndb's api (vndb.org), featuring cache """
	protocol = 1
	def __init__(self, clientname, clientver, username=None, password=None, debug=False):
		self.sock = socket.socket()
		
		if debug: print('Connecting to api.vndb.org')
		self.sock.connect(('api.vndb.org', 19534))
		if debug: print('Connected')
		
		if debug: print('Authenticating')
		if (username == None) or (password == None):
			self.sendCommand('login', {'protocol': self.protocol, 'client': clientname,
				'clientver': float(clientver)})
		else:
			self.sendCommand('login', {'protocol': self.protocol, 'client': clientname,
				'clientver': float(clientver), 'username': username, 'password': password})
		res = self.getRawResponse()
		if res.find('error ') == 0:
			raise vndbException(json.loads(' '.join(res.split(' ')[1:]))['msg'])
		if debug: print('Authenticated')
		
		self.cache = {'get': []}
		self.cachetime = 720 #cache stuff for 12 minutes
	def close(self):
		self.sock.close()		
	def get(self, type, flags, filters, options):
		""" Gets a VN/producer
		
		Example:
		>>> results = vndb.get('vn', 'basic', '(title="Clannad")', '')
		>>> results['items'][0]['image']
		u'http://s.vndb.org/cv/99/4599.jpg'
		"""
		args = '{0} {1} {2} {3}'.format(type, flags, filters, options)
		for item in self.cache['get']:
			if (item['query'] == args) and (time.time() < (item['time'] + self.cachetime)):
				return item['results']
				
		self.sendCommand('get', args)
		res = self.getResponse()[1]
		self.cache['get'].append({'time': time.time(), 'query': args, 'results': res})
		return res

	def sendCommand(self, command, args=None):
		""" Sends a command
		
		Example
		>>> self.sendCommand('test', {'this is an': 'argument'})
		"""
		whole = ''
		whole += command.lower()
		if isinstance(args, basestring):
			whole += ' ' + args
		elif isinstance(args, dict):
			whole += ' ' + json.dumps(args)
		
		self.sock.send('{0}\x04'.format(whole))
	
	def getResponse(self):
		""" Returns a tuple of the response to a command that was previously sent
		
		Example
		>>> self.sendCommand('test')
		>>> self.getResponse()
		('ok', {'test': 0})
		"""
		res = self.getRawResponse()
		cmdname = res.split(' ')[0]
		if len(res.split(' ')) > 1:
			args = json.loads(' '.join(res.split(' ')[1:]))
			
		if cmdname == 'error':
			if args['id'] == 'throttled':
				raise vndbException('Throttled, limit of 100 commands per 10 minutes')
			else:
				raise vndbException(args['msg'])				
		return (cmdname, args)
	def getRawResponse(self):
		""" Returns a raw response to a command that was previously sent 
		
		Example:
		>>> self.sendCommand('test')
		>>> self.getRawResponse()
		'ok {"test": 0}'
		"""
		finished = False
		whole = ''
		while not finished:
			whole += self.sock.recv(4096)
			if '\x04' in whole: finished = True
		return whole.replace('\x04', '').strip()
#######################################################################

class BotModule(object):
	def __init__(self, storage):
		self.storage = storage
		self.admins = {}
		self.bot = None
		self.cut = lambda x: x if x < 200 else x[:200] + '(...)'
		
		self.vndb = VNDB('NiNi IRC Bot', 1.0)
		self.results = []
		self.current = 0
	def register(self):
		return {'functions': [{'vndb': self.cmd_vndb}], 'aliases': {'vn': 'vndb'}}
	def event(self, ev):
		if ev['name'] == 'unload':
			self.vndb.close()

	def cmd_vndb(self, args, receiver, sender):
		"""vndb [name] | {'public': True, 'admin_only': False} | Fetches info on a visual novel"""
		if args == '':
			receiver.msg('Arguments: [(partial) vn name]')
		elif args.strip().lower() == self.bot.cmd_char + 'next':
			self.current += 1
			if len(self.results) == 0:
				receiver.msg('No search results found')
				return
			if (self.current + 1) > len(self.results['items']):
				receiver.msg('End of list')
				return
			
			whole = chr(3) + '07' + self.results['items'][self.current]['title']
			if (self.results['items'][self.current].get('aliases') in ['', None]) == False:
				whole += ' [' + self.results['items'][self.current]['aliases'] + ']'
			whole += chr(15) + ' ' + self.cut(self.results['items'][self.current]['description'].replace('\n', ' ').replace('  ', ' '))
			
			try:
				url = self.bot.modules['google']['instance'].shortenUrl(self.results['items'][0]['image'])
			except:
				url = self.results['items'][0]['image']
			whole += ' ' + chr(3) + '02' + url			
			
			receiver.msg(unicode(whole))
			
		else:
			self.current = 0
			self.results = self.vndb.get('vn', 'basic,details', '(title~"' + args + '")', '')
			
			if len(self.results['items']) == 0:
				receiver.msg(chr(3) + '04Error! ' + chr(15) + 'Nothing found')
				return
			
			whole = chr(3) + '07' + self.results['items'][0]['title']
			if (self.results['items'][0].get('aliases') in ['', None]) == False:
				whole += ' [' + self.results['items'][0]['aliases'] + ']'
			whole += chr(15) + ' ' + self.cut(self.results['items'][0]['description'].replace('\n', ' ').replace('  ', ' '))
			
			try:
				url = self.bot.modules['google']['instance'].shortenUrl(self.results['items'][0]['image'])
			except:
				url = self.results['items'][0]['image']
			whole += ' ' + chr(3) + '02' + url

			
			receiver.msg(unicode(whole))
