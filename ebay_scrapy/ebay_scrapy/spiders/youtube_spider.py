import scrapy
from bs4 import BeautifulSoup
import webbrowser
import urllib2
import requests

class YoutubeSpider(scrapy.Spider):
	name = "youtube"

	allowed_domains = ["youtube.com"]

	start_urls = ["http://www.youtube.com/"]

	def parse(self, response):
		#proxies = { 'http': 'http://root:esfera@123@159.203.255.182/'} 
		# or if it requires authentication 'http://user:pass@host/' instead

		r = requests.get('https://www.youtube.com/?gl=IN')
		text = r.text
		print text
		# proxy_support = urllib2.ProxyHandler({"http":"159.203.255.182"})
		# opener = urllib2.build_opener(proxy_support)
		# urllib2.install_opener(opener)

		# html = urllib2.urlopen("http://www.youtube.com").read()
		# print html
		# print "\n\n url : ", response.url
		# #request = scrapy.Request(url)
		# #request.meta['proxy'] = "http://127.0.0.1"
		# #print "\n\n request : ", request
		# html = response.body
		# soup = BeautifulSoup(html, 'html.parser')
		# print soup.prettify()
		#webbrowser.open(url)
		#chrome_path = 'open -a /Applications/Google\ Chrome.app %s'

		#webbrowser.get(chrome_path).open(response.url)
