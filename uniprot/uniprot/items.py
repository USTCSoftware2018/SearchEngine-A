# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UniprotItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    entry = scrapy.Field()
    entry_name = scrapy.Field()
    reviewed = scrapy.Field()
    protein_names = scrapy.Field()
    gene_names = scrapy.Field()
    organism = scrapy.Field()
    length = scrapy.Field()


class UnirefItem(scrapy.Item):
    cluster_id = scrapy.Field()
    reviewed = scrapy.Field()
    cluster_name = scrapy.Field()
    size = scrapy.Field()
    cluster_members = scrapy.Field()
    organisms = scrapy.Field()
    length = scrapy.Field()
    identity = scrapy.Field()


class UniparcItem(scrapy.Item):
    entry = scrapy.Field()
    organisms = scrapy.Field()
    UniProtKB = scrapy.Field()
    first_seen = scrapy.Field()
    last_seen = scrapy.Field()
    length = scrapy.Field()


class ProteomesItem(scrapy.Item):
    proteome_id = scrapy.Field()
    organism = scrapy.Field()
    organism_id = scrapy.Field()
    protein_count = scrapy.Field()


class TaxonomyItem(scrapy.Item):
    taxon = scrapy.Field()


class ResultItem(scrapy.Item):
    url = scrapy.Field()
    record_num = scrapy.Field()
    hit = scrapy.Field()
    records = scrapy.Field()