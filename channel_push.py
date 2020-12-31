#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telegram.ext import Updater, MessageHandler, Filters
from telegram_util import log_on_fail, splitCommand, matchKey
import random
import threading
import plain_db

with open('credential') as f:
	token = f.read().strip()

tele = Updater(token, use_context=True) # @channel_push_bot
debug_group = tele.bot.get_chat(420074357)
channel_push = tele.bot.get_chat('@channel_push')
channels = plain_db.loadKeyOnlyDB('existing')
recent = plain_db.loadKeyOnlyDB('recent')

@log_on_fail(debug_group)
def handlePrivate(update, context):
	msg = update.effective_message
	if msg.chat.id != debug_group.id:
		return
	command, text = splitCommand(msg.text)
	if matchKey(command, ['remove']):
		result = channels.remove(text)
		msg.reply_text('Removed ' + str(result))
		return
	count = 0
	for piece in msg.text.split():
		if not piece:
			continue
		if piece.startswith('@'):
			count += channels.add('https://t.me/' + piece[1:])
			continue
		if 't.me' in piece:
			count += channels.add(piece)
	msg.reply_text('Added %s items' % count)

def getRandomItem():
	index = random.randint(0, len(channels.items()) - 1)
	return list(channels.items())[index]

@log_on_fail(debug_group)
def sendPush():
	item = getRandomItem()
	if len(recent.items()) * 2 >= len(channels.items()):
		for key in recent.items():
			recent.remove(key)
	while item in recent.items():
		item = getRandomItem()
	recent.add(item)
	channel_push.send_message(item)
	threading.Timer(60 * 60, sendPush).start()

if __name__ == "__main__":
	sendPush()
	tele.dispatcher.add_handler(MessageHandler(Filters.private, handlePrivate))
	tele.start_polling()
	tele.idle()