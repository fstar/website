import random
import base64
# from settings import PROXIES
index = 1
class RandomUserAgent(object):
	"""Randomly rotate user agents based on a list of predefined ones"""
	def __init__(self, agents):
		self.agents = agents
	@classmethod
	def from_crawler(cls, crawler):
		return cls(crawler.settings.getlist('USER_AGENTS'))

	def process_request(self, request, spider):
		#print "**************************" + random.choice(self.agents)
		request.headers.setdefault('User-Agent', random.choice(self.agents))
		# request.headers["referer"] = "https://list.jd.com/list.html?cat=1713,3259&page=24"
