# -*- coding: utf-8 -*-
from urlparse import urljoin

from scrapy import Spider
from scrapy.http import Request

from upcatresults.items import PasserItemLoader


class Upcat2014Spider(Spider):
    name = "upcat2014"
    allowed_domains = ["web.archive.org"]
    start_urls = (
        'http://web.archive.org/web/20140625204215/http://upcat.up.edu.ph/results/',
    )

    def parse(self, response):
        pages = response.xpath('//a[contains(@href, "page-")]/@href').extract()
        for page in pages:
            yield Request(urljoin(response.url, page), self.parse_page)

    def parse_page(self, response):
        passers = response.xpath('//table//tr[count(./td)=4]')
        for passer in passers:
            pil = PasserItemLoader(selector=passer)
            pil.add_xpath('student_number', './td[1]/text()')
            pil.add_xpath('name', './td[2]/text()')
            pil.add_xpath('campus', './td[3]/text()')
            pil.add_xpath('course', './td[4]/text()')
            pil.add_value('source', response.url)
            yield pil.load_item()
