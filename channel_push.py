#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telegram.ext import Updater, MessageHandler, Filters
from telegram_util import log_on_fail
import random
import threading
import plain_db

channels = plain_db.loadNoKeyDB('existing')

with open('credential') as f:
	token = f.read().strip()

tele = Updater(token, use_context=True) # @channel_push_bot
debug_group = tele.bot.get_chat(420074357)
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

@log_on_fail(debug_group)
def sendPush():
	index = random.randint(0, len(channels.items()) - 1)
	channel_push.send_message(list(channels.items())[index])
	threading.Timer(60 * 60, sendPush).start()

if __name__ == "__main__":
	sendPush()
	tele.dispatcher.add_handler(MessageHandler(Filters.private, handlePrivate))
	tele.start_polling()
	tele.idle()