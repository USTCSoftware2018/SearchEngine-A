# -*- coding: utf-8 -*-
import scrapy
import urllib
from rcsb.items import PdbItem, ResultItem
from scrapy.shell import inspect_response

from bs4 import BeautifulSoup


class RcsbSpider(scrapy.Spider):
    name = 'rcsb'
    allowed_domains = ['www.rcsb.org']

    results_to_show_one_time = 20

    argument_tags = {
        'AdvancedKeywordQuery': 'keywords'
    }

    def __init__(self, *args, **kwargs):
        if len(args) > 0:
            raise ValueError
        if 'argument' not in kwargs.keys():
            raise ValueError
        if 'queryType' not in kwargs.keys():
            kwargs['queryType'] = 'AdvancedKeywordQuery'
        if 'sortMethod' not in kwargs.keys():
            kwargs['sortMethod'] = 'rank Descending'
        self.query = kwargs
        self.count = 0
        super(RcsbSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        url = 'https://www.rcsb.org/pdb/rest/search/?sortfield=%s' % urllib.parse.quote(self.query['sortMethod'])
        argument_tag = self.argument_tags[self.query['queryType']]
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        query_text = """
        <orgPdbQuery>
        <queryType>org.pdb.query.simple.%s</queryType>
        <%s>%s</%s>
        </orgPdbQuery>""" % (self.query['queryType'], argument_tag, self.query['argument'], argument_tag)
        yield scrapy.Request(url=url, method='POST', headers=headers, body=query_text, callback=self.entities_parse)

    def entities_parse(self, response):
        # inspect_response(response, self)
        entities = str(response.body).split('\\n')
        entities[0] = entities[0].replace('b\'', '')
        self.count = len(entities)
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en',
            'User-Agent': 'Scrapy/1.5.1 (+https://scrapy.org)',
            'Accept-Encoding': 'gzip,deflate'
        }
        query = ''
        for i in range(self.count):
            query = query + entities[i] + ','
            if (i+1) % self.results_to_show_one_time == 0:
                query = query[0:-1]
                yield scrapy.Request(url="http://www.rcsb.org/pdb/rest/describePDB?structureId=" + query, headers=headers,
                                      callback=self.pdb_parse)
                query = ''
        if query:
            yield scrapy.Request(url="http://www.rcsb.org/pdb/rest/describePDB?structureId=" + query, headers=headers,
                                  callback=self.pdb_parse)

    def pdb_parse(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        result = ResultItem()
        result['record_num'] = self.count
        result['url'] = response.url
        result['records'] = []
        pdbs = soup.select('pdb')
        for pdb in pdbs:
            record = PdbItem()
            record['title'] = pdb.attrs['title']
            record['id'] = pdb.attrs['structureid']
            record['url'] = "https://www.rcsb.org/structure/" + record['id']
            record['last_modified_date'] = pdb.attrs['last_modification_date']
            record['summary'] = pdb.attrs
            result['records'].append(record)
        return result
