import os
import yaml
import time
from telegram_util import commitRepo

last_commit = 0

def commit():
	global last_commit
	if time.time() - last_commit < 20 * 60:
		return
	last_commit = time.time()
	commitRepo()

def getFile(name):
	fn = 'db/' + name
	os.system('touch ' + fn)
	with open(fn) as f:
		return set([x.strip() for x in f.readlines() if x.strip()])

class DBItem(object):
	def __init__(self, name):
		self.items = getFile(name)
		self.fn = 'db/' + name

	def add(self, x):
		x = x.strip()
		if x in self.items:
			return
		self.items.add(x)
		with open(self.fn, 'a') as f:
			f.write('\n' + x)
		commit()

	def remove(self, x):
		raise Exception('To be implemented') 

class DB(object):
	def __init__(self):
		self.reload()

	def reload(self):
		self.existing = DBItem('existing')
		self.blacklist = DBItem('blacklist')
