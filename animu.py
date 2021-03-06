#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import urllib
import urllib2
import re
from HTMLParser import HTMLParser
from PIL import Image
import shutil
try:
	from BeautifulSoup import BeautifulStoneSoup
	from bs4 import BeautifulSoup
	from bs4 import UnicodeDammit
except:
	print 'You must have the python BeautifulSoup module: install pip and execute "pip install beautifulsoup; pip install beautifulsoup4", as root.'
	exit()

from byteformat import format as fmt
import os, inspect
from urllib2 import urlopen
from urllib import quote
from xml.dom import minidom

#----
#MALWrapper was copied from Futaam
#Made by TacticalGenius230 and HarHar
class MALWrapper(object):
	@staticmethod
	def search(name, stype):
		if not stype in ['anime', 'manga']:
			raise TypeError('second parameter must be either "anime" or "manga"') #I know, TypeError isn't meant for that, but meh

		try:
			n = unicodedata.normalize('NFKD', name).encode('ascii','ignore')
		except:
			n = name
		params = urllib.urlencode({'q': n})
		queryurl = 'http://mal-api.com/'+ stype + '/search?%s' % params
		res = urllib2.urlopen(queryurl)
		dict = json.load(res)
		return dict
	@staticmethod
	def details(id, stype):
		if not stype in ['anime', 'manga']:
			raise TypeError('second parameter must be either "anime" or "manga"')
		queryurl = 'http://mal-api.com/'+ stype +'/'+str(id)
		res = urllib2.urlopen(queryurl)
		dict = json.load(res)
		return dict
	@staticmethod
	def getGroupsList(animeId, animeTitle):
		"""Returns a list of tuples in the following form
				[('GroupName', 'details'), ('GroupName', 'details'), ('GroupName', None)]
		"""
		url = 'http://myanimelist.net/anime/' + str(animeId) + '/' + urllib.quote(animeTitle) ##Anime only?
		c = urllib2.urlopen(url).read()
		bs = BeautifulSoup(c)

		smalls = []
		for div in bs.findAll('div'):
			if div.get('class') == ['spaceit_pad']:
				smalls.append(div.findAll('small'))

		x = []
		for tags in smalls:
			if len(tags) != 0:
				if tags[0].getText().startswith('[') == False or tags[0].getText().endswith(']') == False: continue

			if len(tags) > 1:
				x.append((tags[0].getText(), tags[1].getText()))
			elif len(tags) == 1:
				x.append((tags[0].getText(), None))

		return x
	@staticmethod
	def getCharacterList(animeId, animeTitle, stype):
		if not stype in ['anime', 'manga']:
			raise TypeError('second parameter must be either "anime" or "manga"')

		url = 'http://myanimelist.net/'+ stype +'/' + str(animeId) + '/' + urllib.quote(animeTitle) + '/characters'
		c = urllib2.urlopen(url).read().replace("'+'", '').replace("' + '", '')
		bs = BeautifulSoup(c)

		i = 0
		girls = []
		for t in bs.findAll('td')[11:]:
		        try:
		                spl = t.getText().split('\n')
		                if spl[1] in girls:
		                	continue
		                if spl[2].find('Main') != -1 or spl[2].find('Supporting') != -1:
		                        girls.append(spl[1])
		        except:
		                pass
		        i += 1

		d = []
		for b in girls:
			if b.find(',') != -1:
				s = b.split(',')
				b = s[1] + ' ' + s[0]
			d.append(b.lstrip().rstrip().strip('\n'))	        

		ids = []
		for l in bs.findAll('a'):
			try:
				if l.get('href').find('character') == -1: continue
			except:
				continue
			for g in girls:
				try:
					if l.get('href').split('/')[4] in ids:
						continue
					if l.getText() == g:
						ids.append(l.get('href').split('/')[4])
				except:
					continue

		thumbnails = []
		for img in bs.findAll('div'):
			if img.get('class') != ['picSurround']: continue
			try:
				if img.find('a').get('href').find('character') == -1:
					continue		
					print repr(img.find('a').get('href')) + ' - ' + repr(img.find('a').find('img').get('src'))
			except:
				continue

			for g in girls:
				try:
					if img.find('a').find('img').get('src').find('questionmark') == -1 and img.find('a').find('img').get('src') in thumbnails:
						continue
					if img.find('a').get('href').find(g.split(' ')[0]) != -1:
						thumbnails.append(img.find('a').find('img').get('src'))
						continue

					if img.find('a').get('href').find(g.split(' ')[1]) != -1:
						thumbnails.append(img.find('a').find('img').get('src'))
				except:
					continue		

		return (d, ids, thumbnails)
	@staticmethod
	def getCharacterInfo(name, id, raw=False):
		c = urllib2.urlopen('http://myanimelist.net/character/' + str(id))
		d = c.read()

		dammit = UnicodeDammit(d.replace("'+'", '').replace("' + '", ''))

		summary = dammit.unicode_markup.split('<div class="normal_header" style="height: 15px;">' + name)[1]
		summary = summary.split('</div>')[1]
		summary = summary.split('<div')[0]

		jpname = name + dammit.unicode_markup.split('<div class="normal_header" style="height: 15px;">' + name)[1].split('</div>')[0]

		bs = BeautifulSoup(dammit.unicode_markup)

		img = ''
		for image in bs.findAll('img'):
			try:
				if image.get('alt').find(name) != -1:
					img = image.get('src')
					break
			except: continue

		if raw == False:
			return (HTMLEntitiesToUnicode(remove_html_tags(jpname)), HTMLEntitiesToUnicode(remove_html_tags(summary)).rstrip('\n').lstrip('\n'), img)
		else:
			return (jpname, summary, img, name)


class vndbException(Exception):
	pass

class VNDB(object):
	""" Python interface for vndb's api (vndb.org), featuring cache """
	protocol = 1
	def __init__(self, clientname, clientver, username=None, password=None, debug=False):
		if '--no-vndb' in __import__('sys').argv:
			return
		self.sock = socket.socket()
		
		if debug: print('Connecting to api.vndb.org')
		try:
			self.sock.connect(('api.vndb.org', 19534))
		except:
			print('Could not connect to VNDB')
			return
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
#--

class BotModule(object):
	def __init__(self, storage):
		self.storage = storage
		self.admins = {}
		self.bot = None
		self.MAL = MALWrapper()
		self.results = None
		self.i = 0
	def register(self):
		return {'functions': [{'groups': self.cmd_groups}]}
	def event(self, ev):
		pass

	def cmd_groups(self, args, receiver, sender):
		"""groups [anime] | {'public': True, 'admin_only': False} | Returns list of subbing groups for given anime"""
		more = False
		if len(args) == 0: receiver.msg('Missing parameter')

		if args.split(' ')[0].lower() == self.bot.cmd_char + 'next':
			if self.results in [None, []]:
				receiver.msg('You must use the command with an anime name first')
				return

			self.i += 1
			if len(self.results) <= self.i:
				self.i = 0

		else:
			self.results = self.MAL.search(args, 'anime')
			self.i = 0
			if len(self.results) == 0:
				receiver.msg(chr(3) + '5Error!' + chr(15) + ' Anime not found')
				return

			more = True if len(self.results) > 1 else False

		picked = self.results[self.i]
		groups = self.MAL.getGroupsList(picked['id'], picked['title'])

		if len(groups) == 0:
			out = 'No subbing groups found'
		else:
			out = chr(3) + '12Subbing groups for '+ picked['title'] + ': ' + chr(15)
			for group in groups[:len(groups)-1]:
				out += group[0] + ', '
			out = out[:-2]

			if len(groups) != 1:
				out += ' and ' + groups[len(groups)-1][0]

		receiver.msg(out)
		if more:
			receiver.msg('Use "' + self.bot.cmd_char + 'groups ' + self.bot.cmd_char + 'next" to fetch groups from the next anime in the search results')