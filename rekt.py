#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: ndri (https://github.com/ndri/bum-irc-bot/blob/master/modules/uwotm8.py)
import random

class BotModule(object):
	def __init__(self, storage):
		self.storage = storage
		self.admins = {}
		self.bot = None
		self.m8 = ["il bash ye fookin ead in i sware on me mom",
		"if u got sumthn 2 say say it 2 me face",
		"ur a lil gey boi lol i cud own u irl fite me",
		"1v1 fite me irl fgt il rek u",
		"u better shut ur moth u cheeky lil kunt",
		"i swer 2 christ il hook u in the gabber m8",
		"do u evn lift m8?",
		"il rek ur fokn shit i swer 2 christ",
		"il teece u 4 spekin 2 me lik that u little cunt m8",
		"u peelin me onions m8?",
		"yer nothin to me but a cheeky lil dickhead w/ a hot mum & fake bling",
		"ill waste u and smash a fokin bottle oer yer head bruv, i swer 2 christ",
		"ya think u can fokin run ya gabber at me whilst sittin on yer arse behind a lil screen? think again wanka",
		"im callin me homeboys rite now preparin for a proper rumble thatll make ur nan sore jus hearin about it",
		"yer a waste bruv. my homeboys be all over tha place & ill beat ya to a proper fokin pulp with me fists wanka",
		"ill borrow me m8s cricket paddle & see if that gets u the fok out o' newcastle ya daft kunt",
		"ima shite fury & ull drown in it m8. ur in proper mess ya knobhead",
		"il shank ur nan in the tits m8",
		"r u 'avin a giggle ther m8?",
		"i've been at the pub since 4 bong an' im proper pissed m8 i'll toss u in the rubbish bin cuz u've gone off"]
	def register(self):
		return {'functions': [{'rekt': self.cmd_rekt}], 'aliases': {'m8': 'rekt'}}

	def cmd_rekt(self, args, receiver, sender):
		"""rekt | {'public': True, 'admin_only': False} | rekts"""
		if len(args) > 0:
			self.bot.msg(receiver.name, args + '~ ' + random.choice(self.m8))
		else:
			self.bot.msg(receiver.name, random.choice(self.m8))
