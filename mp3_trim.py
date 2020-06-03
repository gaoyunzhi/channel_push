#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import yaml
import os
from telegram.ext import Updater, MessageHandler, Filters
from telegram_util import log_on_fail
from datetime import datetime

with open('credential') as f:
	credential = yaml.load(f, Loader=yaml.FullLoader)

tele = Updater(credential['bot_token'], use_context=True) # @mp3_trim_bot
debug_group = tele.bot.get_chat(420074357)

def fillZero(d):
	x = str(d)
	return '0' * (2 - len(x)) + x

def getOutputName():
	n = datetime.now()   
	return '%s_%s_%s.mp3' % (
		fillZero(n.hour), fillZero(n.minute), fillZero(n.second))

@log_on_fail(debug_group)
def command(update, context):
	msg = update.effective_message
	file = msg.document
	print(1)
	file = file.get_file().download()
	print(2)
	print(file)
	os.system('mkdir tmp')
	os.system('mv %s tmp/%s' % (file, file))
	print(3)
	output_name = 'tmp/' + getOutputName()
	command = '../sox-14.4.2/sox tmp/' + file + ' ' + output_name + \
		' silence 1 0.1 1% -1 0.1 1%'
	print(command)
	os.system(command)
	msg.reply_document(open(output_name,'rb'))
	
if __name__ == "__main__":
	print('===start===')
	tele.dispatcher.add_handler(MessageHandler(Filters.audio, command))
	tele.start_polling()
	tele.idle()