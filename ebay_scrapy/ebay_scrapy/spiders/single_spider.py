import scrapy
from bs4 import BeautifulSoup
from ebay_scrapy.items import EbayProductItem


class SingleSpider(scrapy.Spider):
	name = "sample"
	allowed_domains = ["ebay.co.uk"]
	start_urls = ["http://www.ebay.co.uk/sch/Mobile-and-Smartphones/9355/bn_450671/i.html"]

	def parse(self, response):
		html = response.body
		soup = BeautifulSoup(html, 'html.parser')

		for div in soup.find_all("div", {"id": "ResultSetItems"}):
			for ul in div.find_all("ul", {"id": "ListViewInner"}):
				for li in ul.find_all("li"):
					for h3 in li.find_all("h3"):
						a = h3.find("a")
						link = a["href"]
						yield scrapy.Request(link, callback=self.parse_content)

	def parse_content(self, response):
		html1 = response.body
		soup1 = BeautifulSoup(html1, 'html.parser')

		item = EbayProductItem()

		# name of the product
		h1 = soup1.find("h1", {"id": "itemTitle"})
		title = h1.text
		name = " ".join(title.split()[2:])
		#print "\n\n Product Name : ", name
		item["name"] = name

		# category
		for a in soup1.find_all("a", {"class": "scnd"}):
			category = a.text
			#print "Category : ", category
			item["category"] = category

		#duration of the action
		span = soup1.find("span", {"id": "vi-cdown_timeLeft"})
		if span:
			#print "Duration of the action : ", ' '.join(span.text.split())
			item["duration"] = ' '.join(span.text.split())

		#price
		span1 = soup1.find("span", {"id": "prcIsum"})
		if span1:
			price = span1.string
			item["price"] = price

		div = soup1.find("div", {"class": "u-flL w29 vi-price"})
		span2 = div.find("span", {"id": "prcIsum_bidPrice"})
		if span2:
			price = span2.string
			item["price"] = price
		#print "price : ", price

		#item location
		div1 = soup1.find("div", {"class": "iti-eu-bld-gry "})
		item_location = div1.string
		#print "item location : ", item_location
		item["item_location"] = item_location

		#item specifics
		specific_list = []
		div2 = soup1.find("div", {"class": "section"})
		table = div2.find("table")
		for tr in table.find_all("tr"):
			for td in tr.find_all("td"):
				specific = ' '.join(td.text.split())
				specific_list.append(specific)
		#print "Item specifics : ", specific_list
		item["specifics"] = specific_list

		#return details
		span3 = soup1.find("span", {"id": "vi-ret-accrd-txt"})
		#print "return details : ", span3.string
		item["return_details"] = span3.string

		#condition
		div3 = soup1.find("div", {"id": "vi-itm-cond"})
		condition = div3.string
		item["condition"] = condition

		#item description
		for div4 in soup1.find_all("div", {"class": "itemDescriptionDiv"}):
			for div5 in div4.find_all("div", {"class": ""}):
				p = div5.find("p")
				item["description"] = ' '.join(p.text.split())

		#no of inquiries
		for div6 in soup1.find_all("div", {"id": "why2buy"}):
			for div7 in div6.find_all("div", {"class": "w2b-cnt w2b-3 w2b-brdr"}):
				span = div7.find("span")
				if "inquiries" in span.string:
					item["inquiries"] = span.string

		#where to they ship
		for div8 in soup1.find_all("div", {"class": "u-flL sh-col"}):
			for sp in div8.find_all("span", {"id": "shSummary"}):
				sp1 = sp.find("span", {"id": "fshippingCost"})
				sp2 = sp1.find("span")
				shipping_price = sp2.string
				item["shipping_price"] = shipping_price

				sp3 = sp.find("span", {"id": "fShippingSvc"})
				shipping_location = ' '.join(sp3.text.split())
				item["shipping_location"] = shipping_location

		#quantity
		for spn in soup1.find_all("span", {"class": "qtyTxt vi-bboxrev-dsplblk "}):
			for spn1 in spn.find_all("span", {"id": "qtySubTxt"}):
				spn2 = spn1.find("span")
				if spn2:
					item["quantity"] = ' '.join(spn2.text.split())