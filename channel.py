from bs4 import BeautifulSoup
import cached_url

class Channel(object):
	def __init__(self, link):
		if 'http' not in link:
			link = 'https://' + link
		self.link = link

	def exist(self):
		content = cached_url.get(self.link)
		return 'tgme_page_title' in content

	

		



