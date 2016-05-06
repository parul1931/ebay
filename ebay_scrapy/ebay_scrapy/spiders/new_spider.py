import scrapy
from bs4 import BeautifulSoup
import urllib2
from ebay_scrapy.items import EbayProductItem


class SingleSpider(scrapy.Spider):
	name = "action"
	allowed_domains = ["ebay.co.uk"]
	start_urls = ["http://www.ebay.co.uk/sch/Mobile-and-Smartphones/9355/bn_450671/i.html"]

	def parse(self, response):
		html = response.body
		soup = BeautifulSoup(html, 'html.parser')

		for div in soup.find_all("div", {"class": "pnl-b frmt"}):
			for a in div.find_all("a"):
				if a["href"]:
					link = a["href"]
					if a.text == "Auction":
						yield scrapy.Request(link, callback=self.parse_auction, dont_filter=True)
					else:
						yield scrapy.Request(link, callback=self.parse_now, dont_filter=True)

	def parse_now(self, response):
		html3 = response.body
		soup3 = BeautifulSoup(html3, 'html.parser')

		for div in soup3.find_all("div", {"id": "ResultSetItems"}):
			for ul in div.find_all("ul", {"id": "ListViewInner"}):
				for li in ul.find_all("li"):
					for h3 in li.find_all("h3"):
						a = h3.find("a")
						link = a["href"]
						yield scrapy.Request(link, callback=self.parse_data, dont_filter=True)

	def parse_data(self, response):
		html4 = response.body
		soup4 = BeautifulSoup(html4, 'html.parser')

		item = EbayProductItem()

		link = response.url.split("-/")

		sq_id = link[1].split("?")
		item["sq_id"] = sq_id

		#type of action
		type_of_action = "Buy It Now"
		item["type_of_action"] = type_of_action

		#product name
		h1 = soup4.find("h1", {"id": "itemTitle"})
		title = h1.text
		name = " ".join(title.split()[2:])
		item["name"] = name

		# category
		for a in soup4.find_all("a", {"class": "scnd"}):
			category = a.text
			item["category"] = category

		#duration of the action
		span = soup4.find("span", {"id": "vi-cdown_timeLeft"})
		if span:
			item["duration"] = ' '.join(span.text.split())

		#price
		span1 = soup4.find("span", {"id": "prcIsum"})
		if span1:
			price = span1.string
			item["price"] = price

		div = soup4.find("div", {"class": "u-flL w29 vi-price"})
		span2 = div.find("span", {"id": "prcIsum_bidPrice"})
		if span2:
			price = span2.string
			item["price"] = price
		
		#item location
		div1 = soup4.find("div", {"class": "iti-eu-bld-gry "})
		item_location = div1.string
		item["item_location"] = item_location
		
		#item specifics
		specific_list = []
		spec = dict()
		div2 = soup4.find("div", {"class": "section"})
		table = div2.find("table")
		for tr in table.find_all("tr"):
			for td in tr.find_all("td"):
				specific = ' '.join(td.text.split())
				specific_list.append(specific)
		
		l1 = specific_list[0::2]
		l2 = specific_list[1::2]

		for i in range(len(l1)):
			spec[l1[i]] = l2[i]

		item["specifics"] = spec
		
		#return details
		span3 = soup4.find("span", {"id": "vi-ret-accrd-txt"})
		item["return_details"] = span3.string
		
		#condition
		div3 = soup4.find("div", {"id": "vi-itm-cond"})
		condition = div3.string
		item["condition"] = condition
		
		#item description
		for div4 in soup4.find_all("div", {"class": "itemDescriptionDiv"}):
			for div5 in div4.find_all("div", {"class": ""}):
				p = div5.find("p")
				item["description"] = ' '.join(p.text.split())
				
		#no of inquiries
		for div6 in soup4.find_all("div", {"id": "why2buy"}):
			for div7 in div6.find_all("div", {"class": "w2b-cnt w2b-3 w2b-brdr"}):
				span = div7.find("span")
				if "inquiries" in span.string:
					item["inquiries"] = span.string
			
		#where to they ship
		for div8 in soup4.find_all("div", {"class": "u-flL sh-col"}):
			for sp in div8.find_all("span", {"id": "shSummary"}):
				sp1 = sp.find("span", {"id": "fshippingCost"})
				sp2 = sp1.find("span")
				shipping_price = sp2.string
				item["shipping_price"] = shipping_price
				
				sp3 = sp.find("span", {"id": "fShippingSvc"})
				shipping_location = ' '.join(sp3.text.split())
				item["shipping_location"] = shipping_location
				
		#quantity
		for spn in soup4.find_all("span", {"class": "qtyTxt vi-bboxrev-dsplblk "}):
			for spn1 in spn.find_all("span", {"id": "qtySubTxt"}):
				spn2 = spn1.find("span")
				if spn2:
					item["quantity"] = ' '.join(spn2.text.split())

		#feedback score
		score = soup4.find("div", {"id": "si-fb"})
		item["feedback_score"] = score.text
		
		#no of feedbacks
		div9 = soup4.find("div", {"class": "mbg"})
		a = div9.find("a")
		url = a["href"]

		resp = urllib2.urlopen(url).read()
		data = BeautifulSoup(resp, 'html.parser')

		span = data.find("span", {"class": "all_fb fr"})
		a = span.find("a")
		url1 = a["href"]
		
		html_data = urllib2.urlopen(url1).read()
		soup_data = BeautifulSoup(html_data, 'html.parser')

		td = soup_data.find("td", {"class": "FeedBackStatusLine"})
		item["no_of_feedbacks"] = td.text
		
		#payment method
		dv2 = soup4.find("div", {"id": "payDet1"})
		sp = dv2.find("span")
		sp3 = sp.find("span")
		item["payment_method"] = sp3.text
		#sp4 = dv2.find("span", {"class": "hideGspPymt"})
		#print sp4.text

		#shipping time
		div1 = soup4.find("div", {"class": "sh-del-frst "})
		div2 = div1.find("div")
		item['shipping_time'] = ' '.join(div2.text.split())

		yield item

	def parse_auction(self, response):
		html1 = response.body
		soup1 = BeautifulSoup(html1, 'html.parser')

		for div in soup1.find_all("div", {"id": "ResultSetItems"}):
			for ul in div.find_all("ul", {"id": "ListViewInner"}):
				for li in ul.find_all("li"):
					for h3 in li.find_all("h3"):
						a = h3.find("a")
						link = a["href"]
						yield scrapy.Request(link, callback=self.parse_content, dont_filter=True)
	
	def parse_content(self, response):
		html2 = response.body
		soup2 = BeautifulSoup(html2, 'html.parser')

		item = EbayProductItem()

		link = response.url.split("-/")
		sq_id = link[1].split("?")
		item["sq_id"] = sq_id
		
		#type of action
		type_of_action = "Auction"
		item["type_of_action"] = type_of_action

		#product name
		h1 = soup2.find("h1", {"id": "itemTitle"})
		title = h1.text
		name = " ".join(title.split()[2:])
		item["name"] = name

		# category
		for a in soup2.find_all("a", {"class": "scnd"}):
			category = a.text
			item["category"] = category

		#duration of the action
		span = soup2.find("span", {"id": "vi-cdown_timeLeft"})
		if span:
			item["duration"] = ' '.join(span.text.split())
		
		#price
		span1 = soup2.find("span", {"id": "prcIsum"})
		if span1:
			price = span1.string
			item["price"] = price

		div = soup2.find("div", {"class": "u-flL w29 vi-price"})
		span2 = div.find("span", {"id": "prcIsum_bidPrice"})
		if span2:
			price = span2.string
			item["price"] = price
		
		#item location
		div1 = soup2.find("div", {"class": "iti-eu-bld-gry "})
		item_location = div1.string
		item["item_location"] = item_location

		#item specifics
		specific_list = []
		spec = dict()
		div2 = soup2.find("div", {"class": "section"})
		table = div2.find("table")
		for tr in table.find_all("tr"):
			for td in tr.find_all("td"):
				specific = ' '.join(td.text.split())
				specific_list.append(specific)
		
		l1 = specific_list[0::2]
		l2 = specific_list[1::2]

		for i in range(len(l1)):
			spec[l1[i]] = l2[i]

		item["specifics"] = spec

		#return details
		span3 = soup2.find("span", {"id": "vi-ret-accrd-txt"})
		item["return_details"] = span3.string

		#condition
		div3 = soup2.find("div", {"id": "vi-itm-cond"})
		condition = div3.string
		item["condition"] = condition

		#item description
		for div4 in soup2.find_all("div", {"class": "itemDescriptionDiv"}):
			for div5 in div4.find_all("div", {"class": ""}):
				p = div5.find("p")
				item["description"] = ' '.join(p.text.split())

		#no of inquiries
		for div6 in soup2.find_all("div", {"id": "why2buy"}):
			for div7 in div6.find_all("div", {"class": "w2b-cnt w2b-3 w2b-brdr"}):
				span = div7.find("span")
				if "inquiries" in span.string:
					item["inquiries"] = span.string

		#where to they ship
		for div8 in soup2.find_all("div", {"class": "u-flL sh-col"}):
			for sp in div8.find_all("span", {"id": "shSummary"}):
				sp1 = sp.find("span", {"id": "fshippingCost"})
				sp2 = sp1.find("span")
				shipping_price = sp2.string
				item["shipping_price"] = shipping_price

				sp3 = sp.find("span", {"id": "fShippingSvc"})
				shipping_location = ' '.join(sp3.text.split())
				item["shipping_location"] = shipping_location

		#quantity
		for spn in soup2.find_all("span", {"class": "qtyTxt vi-bboxrev-dsplblk "}):
			for spn1 in spn.find_all("span", {"id": "qtySubTxt"}):
				spn2 = spn1.find("span")
				if spn2:
					item["quantity"] = ' '.join(spn2.text.split())

		#bids
		a = soup2.find("a", {"id": "vi-VR-bid-lnk"})
		link = a["href"]
		span = a.find("span")
		res = urllib2.urlopen(link).read()
		bid_soup = BeautifulSoup(res, 'html.parser')

		bid_list = []
		dic = dict()

		for dv in bid_soup.find_all("div", {"class": "BHbidSecBorderGrey"}):
			table = dv.find("table")
			tr = table.find("tr")
			td = tr.find("td")
			for sp in td.find_all("span"):
				bid_list.append(' '.join(sp.text.split()))

			for dv1 in dv.find_all("div", {"id": "vizrefdiv"}):
				table = dv1.find("table")
				tr = table.find("tr", {"id": "vizRow1"})
				if tr:
					td = tr.find("td", {"class": "contentValueFont"})
					span = td.find("span")
					item["winning_bid_sum"] = span.text
		list1 = bid_list[0::2]
		list2 = bid_list[1::2]
		for i in range(len(list1)):
			dic[list1[i]] = list2[i]

		item["no_of_bids"] = dic["Bids:"]
		item["action_duration"] = dic["Duration:"]
		item["no_of_bidders"] = dic["Bidders:"]

		#feedback score
		score = soup2.find("div", {"id": "si-fb"})
		item["feedback_score"] = score.text

		#no of feedbacks
		div9 = soup2.find("div", {"class": "mbg"})
		a = div9.find("a")
		link = a["href"]

		resp = urllib2.urlopen(link).read()
		data = BeautifulSoup(resp, 'html.parser')

		span = data.find("span", {"class": "all_fb fr"})
		a = span.find("a")
		url = a["href"]
		
		html_data = urllib2.urlopen(url).read()
		soup_data = BeautifulSoup(html_data, 'html.parser')

		td = soup_data.find("td", {"class": "FeedBackStatusLine"})
		item["no_of_feedbacks"] = td.text

		#payment method
		dv2 = soup2.find("div", {"id": "payDet1"})
		for sp in dv2.find_all("span"):
			for sp3 in sp.find_all("span"):
				item["payment_method"] = sp3.text

		#shipping time
		div1 = soup2.find("div", {"class": "sh-del-frst "})
		div2 = div1.find("div")
		item['shipping_time'] = ' '.join(div2.text.split())

		yield item
