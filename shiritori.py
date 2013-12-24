#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gzip
import random

class BotModule(object):
	def __init__(self, storage):
		self.storage = storage
		self.admins = {}
		self.bot = None
		self.dictionary = []

		f = open('/usr/share/dict/words', 'r')
		for word in f.readlines():
			self.dictionary.append(word.lower().replace('\n', ''))
		f.close()

		f = gzip.open('/usr/share/dict/propernames.gz')
		for word in f.readlines():
			self.dictionary.append(word.lower().replace('\n', ''))
		f.close()

		self.playing = {}
	def register(self):
		return {'functions': [{'shiritori': self.cmd_shiritori, 'stop': self.cmd_stop}], 'aliases': {'srtr': 'shiritori'}}
	def event(self, ev):
		if ev['name'] == 'msg':
			split = ev['msg'].lstrip().rstrip().split(' ')
			if len(split) != 1:
				return

			if ev['to'].name in self.playing:
				if self.playing[ev['to'].name]['status'] == 'on':
					if ev['msg'].lower().replace('\'', '').replace(' ', '') == 'imin':
						if ev['from'].nick in self.playing[ev['to'].name]['players']:
							self.bot.msg(ev['to'].name, 'You are already playing, baka')
						else:
							self.bot.msg(ev['to'].name, ev['from'].nick + ' is now playing shiritori! Say "I\'m out" to get out of the game')
							self.playing[ev['to'].name]['players'][ev['from'].nick] = 0
							return
					elif ev['msg'].lower().replace('\'', '').replace(' ', '') == 'imout':
						if ev['from'].nick in self.playing[ev['to'].name]['players']:
							self.bot.msg(ev['to'].name, ev['from'].nick + ' has quit playing shiritori with ' + str(self.playing[ev['to'].name]['players'][ev['from'].nick]) + ' points ;_;')
							del self.playing[ev['to'].name]['players'][ev['from'].nick]
							return
						else:
							self.bot.msg(ev['to'].name, 'You are not playing, baka')
							return

					if ev['from'].nick in self.playing[ev['to'].name]['players']:
						if self.playing[ev['to'].name]['lastword'] == '':
							if split[0].lower() in self.dictionary:
								self.bot.msg(ev['to'].name, 'Alright! Beggining with word "' + split[0] + '"')
								self.playing[ev['to'].name]['lastword'] = split[0].lower()
								self.playing[ev['to'].name]['lastwords'] = [split[0].lower()]
								return
							else:
								self.bot.msg(ev['to'].name, 'That\'s not a word!! Try another one')
								return

						if self.playing[ev['to'].name]['lastword'] == split[0].lower():
							#self.bot.msg(ev['to'].name, 'This word is identical to the last one!')
							return

						if split[0].lower() in self.dictionary:
							match = False
							a = ''
							i = 0
							for letter in split[0].lower():
								a += letter
								i += 1
								if self.playing[ev['to'].name]['lastword'].endswith(a):
									if i >= 2:
										match = True
							if match:
								self.bot.msg(ev['to'].name, ev['from'].nick + ' got it right! +'+ str(len(split[0])) +' points to him')
								self.playing[ev['to'].name]['players'][ev['from'].nick] += len(split[0])
								self.playing[ev['to'].name]['lastword'] = split[0].lower()
								self.playing[ev['to'].name]['lastwords'].append(split[0].lower())
								if len(self.playing[ev['to'].name]['lastwords']) > 20:
									self.playing[ev['to'].name]['lastwords'] = self.playing[ev['to'].name]['lastwords'][1:]
							else:
								#self.bot.msg(ev['to'].name, 'That\'s a valid word, but it did not match end of previous word')
						else:
							#self.bot.msg(ev['to'].name, 'That\'s not a word!')
							pass

	def cmd_shiritori(self, args, receiver, sender):
		"""shiritori | {'public': True, 'admin_only': False} | Starts a game of shiritori"""
		self.bot.msg(receiver.name, sender.nick + ' has started a new game of shiritori, say "I\'m in" to join him')
		self.playing[receiver.name] = {'status': 'on', 'lastword': '', 'lastplayer': '', 'lastwords': [], 'players': {sender.nick: 0}}

	def cmd_stop(self, args, receiver, sender):
		"""stop | {'public': True, 'admin_only': False} | Stops a game of shiritori"""
		if receiver.name in self.playing:
			self.bot.msg(receiver.name, sender.nick + ' has stopped the game')
			del self.playing[receiver.name]
		else:
			self.bot.msg(receiver.name, 'There is no game in place')