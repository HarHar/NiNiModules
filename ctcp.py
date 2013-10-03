#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading
from time import sleep

def waitForCTCP(receiver, nick, pending, time):
	t = 0
	while t < time:
		t += 1
		sleep(1)
		if (nick.lower() in pending) == False: return
	receiver.msg(chr(3) + '07Warning' + chr(15) + ', timeout waiting for CTCP reply'.format(nick))
	del pending[nick.lower()]

class BotModule(object):
	def __init__(self, storage):
		self.storage = storage
		self.admins = {}
		self.bot = None

		self.pending = {}
	def register(self):
		return {'functions': [{'ctcp': self.cmd_ctcp}, {'priv': self.cmd_privset}]}
	def event(self, ev):
		if ev['name'] == 'msg':
			if len(ev['msg']) == 0: return
			if ev['msg'][0] == chr(1) and ev['from'].nick.lower() in self.pending:
				split = ev['msg'].replace(chr(1), '').split(' ')
				x = ''
				for w in split[1:]:
					x += w + ' '
				x = x[:-1]
				self.bot.msg(self.pending[ev['from'].nick.lower()], 'CTCP ' + chr(2) + split[0] + chr(15) + ' reply from ' + ev['from'].nick + ': ' + x)
				del self.pending[ev['from'].nick.lower()]

	def cmd_ctcp(self, args, receiver, sender):
		"""ctcp [nick] [type] | {'public': True, 'admin_only': False} | Sends a ctcp to the desired nick and shows return"""
		s = args.split(' ')
		if len(s) != 2:
			receiver.msg(chr(2) + 'Usage:' + chr(15) + ' ' + self.bot.cmd_char + 'ctcp [nick] [type]')
			return

		if s[0].lower() in self.pending:
			receiver.msg(chr(3) + '05Error' + chr(15) + ' already waiting for CTCP reply from user')
			return

		self.bot.msg(s[0], chr(1) + s[1].upper() + ' ' + chr(1))
		self.pending[s[0].lower()] = receiver.name
		
		thread = threading.Thread(target=waitForCTCP, args=(receiver, sender.nick, self.pending, 10))
		thread.setDaemon(True)
		thread.start()

	def cmd_privset(self, args, receiver, sender):
		"""priv [on/off] | {'public': False, 'admin_only': False} | Turns CTCP privacy on or off"""
		receiver.msg('404 Not Implemented')
