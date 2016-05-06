# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class EbayScrapyItem(scrapy.Item):
	category = scrapy.Field()
	name = scrapy.Field()
	link = scrapy.Field()


class EbayProductItem(scrapy.Item):
	name = scrapy.Field()
	category = scrapy.Field()
	duration = scrapy.Field()
	price = scrapy.Field()
	item_location = scrapy.Field()
	specifics = scrapy.Field()
	return_details = scrapy.Field()
	condition = scrapy.Field()
	description = scrapy.Field()
	inquiries = scrapy.Field()
	shipping_price = scrapy.Field()
	shipping_location = scrapy.Field()
	quantity = scrapy.Field()
	type_of_action = scrapy.Field()
	action_duration = scrapy.Field()
	no_of_bids = scrapy.Field()
	no_of_bidders = scrapy.Field()
	winning_bid_sum = scrapy.Field()
	feedback_score = scrapy.Field()
	no_of_feedbacks = scrapy.Field()
	payment_method = scrapy.Field()
	shipping_time = scrapy.Field()
	sq_id = scrapy.Field()

	