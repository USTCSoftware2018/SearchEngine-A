# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PdbItem(scrapy.Item):
    title = scrapy.Field()
    id = scrapy.Field()
    url = scrapy.Field()
    last_modified_date = scrapy.Field()
    summary = scrapy.Field()


class ResultItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    record_num = scrapy.Field()
    records = scrapy.Field()
