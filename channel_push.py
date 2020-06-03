#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import yaml
from telegram.ext import Updater, MessageHandler, Filters
from telegram_util import log_on_fail
from channel import Channel
import os
import time
from db import DB
import random

HELP_MESSAGE = '''
Please send me the channel/group you recommend, we support batch send.
'''

with open('credential') as f:
	credential = yaml.load(f, Loader=yaml.FullLoader)

tele = Updater(credential['bot_token'], use_context=True) # @channel_push_bot
debug_group = tele.bot.get_chat(420074357)
db = DB()
push_channel = tele.bot.get_chat('@channel_push')

def findChannels(text):
	result = []
	for x in text.split():
		if not x:
			continue
		if x.startsWith('@'):
			result.append(Channel('https://t.me/' + x[1:]))
			continue
		if 't.me' in x:
			result.append(Channel(x))
			continue
	result = [x for x in result if x.exist()]
	[x.save() for x in result]
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
	removeOldFiles('tmp')
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
	
@log_on_fail(debug_group)
def sendPush():
	global db_pos
	db_pos += 1
	channel_push.send_text(random.sample(db.existing.items))
	if 'test' in sys.args:
		interval = 10
	else:
		interval = 60 * 60
	threading.Timer(interval, lambda: os.system(sendPush)).start()

if __name__ == "__main__":
	sendPush()
	tele.dispatcher.add_handler(MessageHandler(Filters.private, handlePrivate))
	tele.start_polling()
	tele.idle()