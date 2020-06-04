#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import yaml
from telegram.ext import Updater, MessageHandler, Filters
from telegram_util import log_on_fail, commitRepo
from channel import Channel
import os
import time
from db import DB
import random
import sys
import threading

HELP_MESSAGE = '''
Please send me the channel/group you recommend, we support batch send.
'''

with open('credential') as f:
	credential = yaml.load(f, Loader=yaml.FullLoader)

tele = Updater(credential['bot_token'], use_context=True) # @channel_push_bot
debug_group = tele.bot.get_chat(420074357)
db = DB()
channel_push = tele.bot.get_chat('@channel_push')

def findChannels(text):
	result = []
	for x in text.split():
		if not x:
			continue
		if x.startswith('@'):
			result.append(Channel('https://t.me/' + x[1:]))
			continue
		if 't.me' in x:
			result.append(Channel(x))
			continue
	result = [x for x in result if x.exist()]
	[x.save(db) for x in result]
	return result

def removeOldFiles(d):
	try:
		for x in os.listdir(d):
			if os.path.getmtime(d + '/' + x) < time.time() - 60 * 60 * 72 or \
				os.stat(d + '/' + x).st_size < 400:
				os.system('rm ' + d + '/' + x)
	except:
		pass

@log_on_fail(debug_group)
def handlePrivate(update, context):
	msg = update.effective_message
	if not msg.text:
		msg.reply_text(HELP_MESSAGE)
		return
	channels = findChannels(msg.text)
	if not channels:
		msg.reply_text('no channel/group found.\n' + HELP_MESSAGE)
		return
	channel_list = [x.getLink() for x in channels]
	msg.reply_text('Channels/groups recorded:\n' + '\n'.join(channel_list))
	
def recordList():
	channel_list = [Channel(x).getRep() for x in db.existing.items]
	with open('db/channels.md', 'w') as f:
		f.write('\n\n'.join(channel_list))

@log_on_fail(debug_group)
def sendPush():
	channel_push.send_message(random.choice(db.existing.items))
	if random.random() < 0.05:
		removeOldFiles('tmp')
		recordList()
		commitRepo()
	if 'test' in sys.argv:
		interval = 10
	else:
		interval = 60 * 60
	threading.Timer(interval, sendPush).start()

if __name__ == "__main__":
	recordList()
	sendPush()
	tele.dispatcher.add_handler(MessageHandler(Filters.private, handlePrivate))
	tele.start_polling()
	tele.idle()