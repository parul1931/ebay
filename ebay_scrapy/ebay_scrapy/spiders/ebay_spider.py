import scrapy
from ebay_scrapy.items import EbayScrapyItem, EbayProductItem
from bs4 import BeautifulSoup


class EbaySpider(scrapy.Spider):

	name = "ebay"
	allowed_domains = ["ebay.co.uk"]
	start_urls = ["http://www.ebay.co.uk/rpp/electronics"]
	
	def parse(self, response):
		html = response.body
		soup = BeautifulSoup(html, 'html.parser')

		#item = EbayScrapyItem()

		for div in soup.find_all("div", {"class": "nav"}):
			h1 = div.find("h1", {"id": "mainTitle"})
			#print "\n\n name : ", h1.text
			#item["category"] = h1.text

			for ul in div.find_all("ul", {"class": "widget navigation-list main-navigation"}):
				li = ul.find("li")
				ul1 = li.find("ul", {"class": "navigation-list"})
				for li in ul1.find_all("li"):
					for a in li.find_all("a", {"class": "title-block"}):
						link  = a['href']
						print "\n\n link in parse : ", link
						#item["link"] = link
						#span =a.find("span", {"class": "title"})
						#title = span.text
						#item["name"] = title
						#yield item
						yield scrapy.Request(link, callback=self.parse_content)


	def parse_content(self, response):
		html1 = response.body
		soup1 = BeautifulSoup(html1, 'html.parser')

		for div in soup1.find_all("div", {"class": "nav"}):
			for ul in div.find_all("ul", {"class": "widget navigation-list main-navigation"}):
				li = ul.find("li")
				ul1 = li.find("ul", {"class": "navigation-list"})
				for li in ul1.find_all("li"):
					for a in li.find_all("a", {"class": "title-block"}):
						link  = a['href']
						print "\n\n link in parse content: ", link
						#item["link"] = link
						#span =a.find("span", {"class": "title"})
						#title = span.text
						#item["name"] = title
						#yield item
						yield scrapy.Request(link, callback=self.parse_data)

	def parse_data(self, response):
		html2 = response.body
		soup2 = BeautifulSoup(html2, 'html.parser')

		for div in soup2.find_all("div", {"class": "pnl-b frmt"}):
			for a in div.find_all("a"):
				if a["href"]:
					link = a["href"]
					title = a.string
					#print "\n\n\n title : ", title
					#print "link : ", link
					yield scrapy.Request(link, callback=self.details)

	def details(self, response):
		html3 = response.body
		soup3 = BeautifulSoup(html3, 'html.parser')

		for div in soup3.find_all("div", {"id": "ResultSetItems"}):
			for ul in div.find_all("ul", {"id": "ListViewInner"}):
				for li in ul.find_all("li"):
					for h3 in li.find_all("h3"):
						a = h3.find("a")
						if a.string:
							title = a.string
							url = a["href"]
							yield scrapy.Request(url, callback=self.contents)

	def contents(self, response):
		html4 = response.body
		soup4 = BeautifulSoup(html4, 'html.parser')

		item = EbayProductItem()

		h1 = soup4.find("h1", {"id": "itemTitle"})
		title = h1.text
		name = " ".join(title.split()[2:])
		item["name"] = name
		item["specifics"] = []
		#div = soup4.find("div", {"class": "itemAttr"})
		div = soup4.find("div", {"class": "section"})
		table = div.find("table")
		for tr in table.find_all("tr"):
			for td in tr.find_all("td"):
				specific = ' '.join(td.text.split())
				item["specifics"].append(specific)
		for a in soup4.find_all("a", {"class": "scnd"}):
			item["category"] = a.text

		span = soup4.find("span", {"id": "prcIsum"})
		if span:
			price = span.string
		
		div = soup4.find("div", {"class": "u-flL w29 vi-price"})
		span1 = div.find("span", {"id": "prcIsum_bidPrice"})
		if span1:
			price = span1.string
		item["price"] = price

		div1 = soup4.find("div", {"class": "iti-eu-bld-gry "})
		item_location = div1.string
		item["item_location"] = item_location
		yield item		
