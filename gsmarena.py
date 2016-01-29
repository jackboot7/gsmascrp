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


class GSMArenaSpider(scrapy.Spider):
    # A bunch of hardcoded configuration here as it being my first scrapy
    # spider, based on tutorial.

    name = 'gsmarena'
    start_urls = ['http://www.gsmarena.com/makers.php3']

    def parse(self, response):
        # I make a set of URLs in order to avoid duplicated URLs.
        # As the brands generator blindly yield each column, it will produce
        # the column with the brand logo (which has a link) and the column with
        # the link itself.

        brand_urls = {brand.css('a::attr(href)').extract()[0] for brand in brands(response)}

        # I really miss the yield from syntax from Python3 :'(
        for url in brand_urls:
            full_url = response.urljoin(url)
            yield scrapy.Request(full_url, callback=self.parse_brand)

    def parse_brand(self, response):  # TODO
        # Note: I would like to "download" the whole page.
        yield {'data': response}
