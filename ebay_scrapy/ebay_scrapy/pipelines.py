# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class EbayScrapyPipeline(object):
    def process_item(self, item, spider):
        with open("data.txt", "a") as f:
        	data = "%s \n\n" % str(item)
        	f.write(data.encode("UTF-8"))
        return item
        
