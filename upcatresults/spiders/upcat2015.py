# -*- coding: utf-8 -*-
from urlparse import urljoin

from scrapy import Spider
from scrapy.http import Request

from upcatresults.items import PasserItemLoader


class Upcat2015Spider(Spider):
    name = "upcat2015"
    allowed_domains = ["upcat.up.edu.ph"]
    start_urls = (
        'http://upcat.up.edu.ph/results/',
    )

    def parse(self, response):
        pages = response.xpath('//a[contains(@href, "page-")]/@href').extract()
        for page in pages:
            yield Request(urljoin(response.url, page), self.parse_page)

    def parse_page(self, response):
        passers = response.xpath('//table//tr[count(./td)=3]')
        for passer in passers:
            pil = PasserItemLoader(selector=passer)
            pil.add_xpath('name', './td[1]/text()')
            pil.add_xpath('campus', './td[2]/text()')
            pil.add_xpath('course', './td[3]/text()')
            pil.add_value('source', response.url)
            yield pil.load_item()
