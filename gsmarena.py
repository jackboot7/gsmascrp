# -*- coding:utf8 -*-
'''
This spider simply visit each brand page from gsmarena.com

Implementing parse_brand, you can stablish what to do with each page.
'''

import scrapy


def brands(response):   # This could be rewrited as a 'flattern' function
                        # which simply convert an html table in a iterable of
                        # columns
    for row in response.css('.st-text table tr'):
        for col in row.css('td'):
            yield col


def phones(response): # Same as brands. I would like it to be a li generator.

    for li in response.css('#review-body li'):
        yield li

def spec_detail(spec_row):

    spec = {}
    spec['type'] = 'spec'
    spec['name'] = spec_row.css('td').extract()[0]
    spec['value'] = spec_row.css('td').extract()[1]

    return spec

def specs_class_specs(specs_class_table):

    for spec_row in specs_class_table.css('tr'):
        yield spec_detail(spec_row)

def specs_class(specs_class_table):

    specs_class = {}
    specs_class['type'] = 'class'
    specs_class['name'] = specs_class_table.css('th').extract_first()
    specs_class['specs'] = list(specs_class_specs(specs_class_table))


def phone_specs(response):

    specs_list = response.css('#specs-list')
    for specs_class_table in specs_list.css('table'):
        yield specs_class(specs_class_table)

class GSMArenaSpider(scrapy.Spider):
    # A bunch of hardcoded configuration here as it being my first scrapy
    # spider, based on tutorial.

    name = 'gsmarena'
    # start_urls = ['http://www.gsmarena.com/makers.php3']
    # start_urls = ['http://www.gsmarena.com/yu-phones-100.php']
    start_urls = ['file:///home/jgomo3/workspace/scrapy-tuto/samsung_galaxy_v_plus-7395.html']

    def parse(self, response):
        for element in self.parse_phone(response):
            yield element

    def parse_root(self, response):
        # I make a set of URLs in order to avoid duplicated URLs.
        # As the brands generator blindly yield each column, it will produce
        # the column with the brand logo (which has a link) and the column with
        # the link itself.

        brand_urls = {brand.css('a::attr(href)').extract()[0] for brand in brands(response)}

        # I really miss the yield from syntax from Python3 :'(
        for url in brand_urls:
            full_url = response.urljoin(url)
            yield scrapy.Request(full_url, callback=self.parse_brand)

    def parse_brand(self, response): #TODO: Do pagination

        phone_urls = {phone.css('a::attr(href)').extract()[0] for phone in phones(response)}

        for url in phone_urls:
            full_url = response.urljoin(url)
            yield scrapy.Request(full_url, callback=self.parse_phone)

    def parse_phone(self, response):
        phone = {}
        phone['type'] = 'phone'
        phone['name'] = response.css('h1.specs-phone-name-title::text').extract_first()
        phone['specs'] = list(phone_specs(response))
        yield phone


