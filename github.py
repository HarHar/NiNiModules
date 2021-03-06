#!/usr/bin/env python
# -*- coding: utf-8 -*-
import httplib2
from urllib import quote
import json
from StringIO import StringIO

class BotModule(object):
	def __init__(self, storage):
		self.storage = storage
		self.admins = {}
		self.bot = None
	def register(self):
		return {'functions': [{'github': self.cmd_github, 'language': self.cmd_language}], 'aliases': {'gh': 'github', 'lang': 'language'}}
	def event(self, ev):
		#to parse URLs
		pass

	def cmd_language(self, args, receiver, sender):
		"""github [user] | {'public': True, 'admin_only': False} | Gets GitHub info and statistics on user"""
		if args.replace(' ', '') == '':
			user = sender.nick
		else:
			user = quote(args)

		queryurl = 'https://api.github.com/users/' + user + '/repos?sort=pushed'
		conn = httplib2.Http(disable_ssl_certificate_validation=True)
		try:
			auth = base64.encodestring(githubCredentials[0] + ':' + githubCredentials[1])
		except NameError:
			auth = ''

		if auth != '':
			(response, content) = conn.request(queryurl, 'GET', headers = {'Authorization': 'Basic ' + auth})
		else:
			(response, content) = conn.request(queryurl)
		io = StringIO(content)
		dic = json.load(io)

		queryurl = 'https://api.github.com/users/' + user
		conn = httplib2.Http(disable_ssl_certificate_validation=True)
		if auth != '':
			(response, content) = conn.request(queryurl, 'GET', headers = {'Authorization': 'Basic ' + auth})
		else:
			(response, content) = conn.request(queryurl)
		io = StringIO(content)
		udic = json.load(io)

		if dic.__contains__('message') == True:
			receiver.msg('Error: ' + dic['message'])
			return

		if udic.__contains__('message') == True:
			receiver.msg('Error: ' + udic['message'])
			return

		try:
			if udic['name'] == None:
				udic['name'] = udic['login']
		except KeyError:
			udic['name'] = udic['login']

		fave = ''
		languages = {}
		for repo in dic:
			if languages.get(repo['language']) == None:
				languages[repo['language']] = 1
			else:
				languages[repo['language']] += 1
		if len(languages) != 0:
			highest = ('None', 0)

			for l in languages:
				if languages[l] > highest[1]:
					highest = (l, languages[l])
			fave = str(highest[0])
			if fave == 'None': fave = ''

			if fave == 'Python':
				fave = chr(3) + '02' + fave.upper() + '!!' + chr(15)
			elif fave.lower() in ['javascript', 'c#', 'java', 'html', 'css']:
				fave = chr(3) + '03>' + fave + chr(15)

		if fave != '':
			receiver.msg(udic['name'] + '\'s favorite language: ' + chr(2) + fave)
		else:
			receiver.msg('Unknown language; 2obscure or non-existant')
				
	def cmd_github(self, args, receiver, sender):
		"""github [user] | {'public': True, 'admin_only': False} | Gets GitHub info and statistics on user"""
		if args.replace(' ', '') == '':
			user = sender.nick
		else:
			user = quote(args)

		queryurl = 'https://api.github.com/users/' + user + '/repos?sort=pushed'
		conn = httplib2.Http(disable_ssl_certificate_validation=True)
		try:
			auth = base64.encodestring(githubCredentials[0] + ':' + githubCredentials[1])
		except NameError:
			auth = ''

		if auth != '':
			(response, content) = conn.request(queryurl, 'GET', headers = {'Authorization': 'Basic ' + auth})
		else:
			(response, content) = conn.request(queryurl)
		io = StringIO(content)
		dic = json.load(io)

		queryurl = 'https://api.github.com/users/' + user
		conn = httplib2.Http(disable_ssl_certificate_validation=True)
		if auth != '':
			(response, content) = conn.request(queryurl, 'GET', headers = {'Authorization': 'Basic ' + auth})
		else:
			(response, content) = conn.request(queryurl)
		io = StringIO(content)
		udic = json.load(io)

		if dic.__contains__('message') == True:
			receiver.msg('Error: ' + dic['message'])
			return

		if udic.__contains__('message') == True:
			receiver.msg('Error: ' + udic['message'])
			return

		try:
			if udic['name'] == None:
				udic['name'] = udic['login']
		except KeyError:
			udic['name'] = udic['login']
		try:
			if udic['blog'] == None or udic['blog'] == '':
				udic['blog'] = 'no website'
		except KeyError:
			udic['blog'] = 'no website'
		try:
			if udic['email'] == None:
				udic['email'] = 'no public email'
		except KeyError:
			udic['email'] = 'no public email'
		try:
			if udic['bio'] == None:
				udic['bio'] = udic['type']
		except KeyError:
			udic['bio'] = udic['type']
		try:
			if udic['location'] == None:
				udic['location'] = 'nowhere'
		except KeyError:
			udic['location'] = 'nowhere'
		try:
			if udic['gravatar_id'] == None:
				udic['gravatar_id'] = 'non-existant-email'
		except KeyError:
			udic['gravatar_id'] = 'non-existant-email'

		try:
			gravatar = self.bot.modules['google']['instance'].shortenUrl('http://www.gravatar.com/avatar/' + udic['gravatar_id'] + '?s=200')
		except:
			gravatar = 'http://www.gravatar.com/avatar/' + udic['gravatar_id'] + '?s=200'
		c = ''
		if udic.__contains__('company'):
			if udic['company'] != None:
				c = chr(3) + '14 [' + udic['company'] + ']' + chr(15)

		fave = ''
		languages = {}
		for repo in dic:
			if languages.get(repo['language']) == None:
				languages[repo['language']] = 1
			else:
				languages[repo['language']] += 1
		if len(languages) != 0:
			highest = ('None', 0)

			for l in languages:
				if languages[l] > highest[1]:
					highest = (l, languages[l])
			fave = str(highest[0])
			if fave == 'None': fave = ''

			if fave == 'Python':
				fave = chr(3) + '02' + fave.upper() + '!!' + chr(15)
			elif fave.lower() in ['javascript', 'c#', 'java', 'html', 'css']:
				fave = chr(3) + '03>' + fave + chr(15)

		if fave != '':
			fave = ' |' + chr(3) + '7 Favorite language: ' + fave + chr(15)

		receiver.msg(chr(15) + chr(2) + udic['name'] + chr(15) + c + ' |' + chr(3) + '7 ' + udic['blog'] + chr(15) + ' |' + chr(3) + '4 ' + udic['location'] + chr(15) + ' |' + chr(3) + '7 ' + udic['email'] + chr(15) + ' |' + chr(3) + '4 ' + str(udic['public_gists']) + ' public gists' + chr(15) + ' |' + chr(3) + '7 ' + str(udic['public_repos']) + ' public repos' + chr(15) + ' |' + chr(3) + '4 ' + str(udic['followers']) + ' followers' + chr(15) + ' |' + chr(3) + '7 ' + str(udic['following']) + ' following' + chr(15) + ' |' + chr(3) + '4 Avatar: ' + gravatar + chr(15) + fave)

	##############
	#Web Page
	##############
	def http(self, path, handler):
		return {'title': 'Example web page', 'content': '<p class="lead">This is a cute example page :3</p><p>It looks like you are on the page ' + path + '..</p>'}