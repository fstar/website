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
		request.headers.setdefault('cookie', '''TrackID=1YJf-2dIp9ahAOzUIEKv13v4OlMeEyHXNaj0-kexWwwZFHQXpE2ck_ueFTsPJUSzNAs-UHFU3UjW8JpwBoyRvq19yXhAIwbnmqHSqUXUoxlFkvNDQFt4vbtcTsI5jZdIk; pinId=DkQjdZAPprlBmRHLQBnFbrV9-x-f3wj7; unpl=V2_ZzNtbRFWEEdzD05RckxfDGIEElxLU0pHc1pFVX0cVVEzURIPclRCFXMUR1RnGl8UZwIZXEpcQxxFCHZXchBYAWcCGllyBBNNIEwHDCRSBUE3XHxcFVUWF3RaTwEoSVoAYwtBDkZUFBYhW0IAKElVVTUFR21yVEMldQl2VnwYXARgAhtYcmdEJUU4RlZ6GVwHVwIiXHIVF0l3CUNXchkRB2ACElxFVkoQRQl2Vw%3d%3d; __jdv=122270672|baidu-pinzhuan|t_288551095_baidupinzhuan|cpc|0f3d30c8dba7459bb52f2eb5eba8ac7d_0_b0bc76948d284610858c7c20748eec1c|1485065398857; areaId=2; ipLoc-djd=2-2813-51976-0; ipLocation=%u4E0A%u6D77; listck=fabb66020a5b772dd2b204ac53a7ade2; __jda=122270672.360106084.1455325780.1485071978.1485136663.59; __jdb=122270672.7.360106084|59.1485136663; __jdc=122270672; __jdu=360106084''')
		request.headers.setdefault('accept',"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8")
		# request.headers["referer"] = "https://list.jd.com/list.html?cat=1713,3259&page=24"
