#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import yaml
from telegram.ext import Updater, MessageHandler, Filters
from telegram_util import log_on_fail

HELP_MESSAGE = '''
Please send me the channel/group you recommend, we support batch send.
'''

with open('credential') as f:
	credential = yaml.load(f, Loader=yaml.FullLoader)

tele = Updater(credential['bot_token'], use_context=True) # @channel_push_bot
debug_group = tele.bot.get_chat(420074357)


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
	
if __name__ == "__main__":
	tele.dispatcher.add_handler(MessageHandler(Filters.private, handlePrivate))
	tele.start_polling()
	tele.idle()