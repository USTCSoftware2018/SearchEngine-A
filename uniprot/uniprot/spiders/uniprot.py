# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector

from uniprot.items import ResultItem, UniprotItem, UnirefItem, UniparcItem, ProteomesItem, TaxonomyItem

import urllib


class UniprotSpider(scrapy.Spider):
    name = 'uniprot'
    allowed_domains = ['www.uniprot.org']
    tags = {
        'uniprot': [
            'entry',
            'entry_name',
            'reviewed',
            'protein_names',
            'gene_names',
            'organism',
            'length'
        ],
        'uniref': [
            'cluster_id',
            'reviewed',
            'cluster_name',
            'size',
            'cluster_members',
            'organisms',
            'length',
            'identity'
        ],
        'uniparc': [
            'entry',
            'organisms',
            'UniProtKB',
            'first_seen',
            'last_seen',
            'length'
        ],
        'proteomes':[
            'proteome_id',
            'organism',
            'organism_id',
            'protein_count'
        ],
        'taxonomy':[
            'taxon'
        ]
    }
    items = {
        'uniprot': UniprotItem,
        'uniref': UnirefItem,
        'uniparc': UniparcItem,
        'proteomes': ProteomesItem,
        'taxonomy': TaxonomyItem
    }

    def __init__(self, *args, **kwargs):
        if len(args) > 0:
            raise ValueError
        if 'query' not in kwargs.keys():
            raise ValueError
        if 'sort' not in kwargs.keys():
            kwargs['sort'] = 'score'
        self.query_dict = kwargs
        self.query = urllib.parse.urlencode(kwargs)
        super(UniprotSpider, self).__init__()

    def start_requests(self):
        base = "https://www.uniprot.org"

        headers = {'User-Agent': 'Python', 'email': 'guanxiux@mail.ustc.edu.cn', "Accept": 'application/xml'}

        dbs = [
            '/uniprot/?',
            '/uniref/?',
            '/uniparc/?',
            '/proteomes/?',
            '/taxonomy/?'
        ]

        for i in range(len(dbs)):
            yield scrapy.FormRequest(base + dbs[i] + self.query, headers=headers, callback=self.parse)

    def result_init(self, response):
        body = Selector(text=response.body)
        result = ResultItem()
        result['url'] = response.url
        result['record_num'] = body.xpath('//strong[@ class=$val]/text()', val="queryResultCount").extract_first()
        if not result['record_num'] and response.url.split('/')[-1] == self.query_dict['query']:
            result['hit'] = True
        else:
            result['hit'] = False
        result['records'] = []
        return result, body

    def bind_url(self, selector):
        if len(selector.xpath('.//@href')) > 0:
            return {selector.xpath('.//text()').extract_first(): selector.xpath('.//@href').extract_first()}
        elif len(selector.xpath('.//text()')) > 0:
            return selector.xpath('.//text()').extract_first()
        else:
            return selector.xpath('.//@title').extract_first()

    def crawl_row(self, tags, column_range, row_selector, item):
        columns = row_selector.xpath('./td')
        for i in column_range:
            cell = []
            lines = columns[i].xpath('./*')
            if len(lines) > 0:
                for line in lines:
                    cell.append(self.bind_url(line))
            else:
                cell.append(self.bind_url(columns[i]))
            item[tags[i-1]] = cell
        return item

    def parse(self, response):
        type = response.url.split('/')[-2]
        tags = self.tags[type]
        result, body = self.result_init(response)
        # query的值是一个确定的entry_id时, 重定向到了详情页, 暂时还没做详情页的爬取
        if result['hit']:
            yield result
        for tr in body.xpath('//tbody/tr'):
            item = self.crawl_row(tags, range(1,len(tags) + 1), tr, self.items[type]())
            result['records'].append(item)
        yield result
        # 翻页功能, 还不太熟悉
        # next_page = body.xpath('.//a[@class=$val]/@herf', val='nextPageLink').extract_first()
        # if next_page:
        #     next_page = response.urljoin(next_page)
        #     yield response.follow(next_page, callback=self.parse)
