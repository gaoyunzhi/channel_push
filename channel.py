from bs4 import BeautifulSoup
import cached_url
from telegram_util import matchKey

def getCount(text):
	print('getCount', text)
	try:
		return int(''.join(text.split()[:-1]))
	except:
		return 0

class Channel(object):
	def __init__(self, link):
		if 'http' not in link:
			link = 'https://' + link
		self.link = link

	def exist(self):
		content = cached_url.get(self.link, force_cache=True)
		return 'tgme_page_title' in content

	def passing(self, db):
		content = cached_url.get(self.link, force_cache=True)
		soup = BeautifulSoup(content, 'html.parser')
		member = soup.find('div', class_='tgme_page_extra')
		if not member:
			return False
		description = soup.find('div', class_='tgme_page_description').text
		if matchKey(description, db.blacklist.items):
			return False
		member_block = member.text.split(',')
		print('member_block', member_block)
		if len(member_block) > 1:
			return getCount(member_block[1]) > 10
		return getCount(member_block[0]) > 150

	def save(self, db):
		if not self.passing(db):
			return
		db.existing.add(self.link)

	def getLink(self):
		# TODO: with channel name?
		return self.link