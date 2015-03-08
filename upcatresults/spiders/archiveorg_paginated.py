# -*- coding: utf-8 -*-
import re
from urlparse import urljoin

from scrapy import Spider
from scrapy.http import Request

from upcatresults.items import PasserItemLoader


START_URLS = {
    '2014': 'http://web.archive.org/web/20140625204215/http://upcat.up.edu.ph/results/',
    '2013': 'http://web.archive.org/web/20130310194916/http://upcat.up.edu.ph/results/',
    '2012': 'http://web.archive.org/web/20120123031805/http://www.creativepointonline.com/upcat/',
    '2011': 'http://web.archive.org/web/20110103215432/http://upcat.stickbreadsolutions.com/',
    '2010': 'http://web.archive.org/web/20100130062527/http://upcat.up.edu.ph/results/',
}

class UpcatArvhiceOrgSearchSpider(Spider):
    name = "upcat_archiveorg_search"
    allowed_domains = ["web.archive.org"]
    which_year = None

    URL_RE = re.compile(r'http://web\.archive\.org/web/\d+/(.*)')

    def start_requests(self):
        if self.which_year:
            for i in range(ord('A'), ord('Z') + 1):
                yield Request(
                    'http://web.archive.org/web/%s0714131655/http://upcat.up.edu.ph/cgi-bin/results.cgi?s=%s' % (
                        self.which_year, chr(i)
                    )
                )
    def parse(self, response):
        year = response.xpath('//font[@size="5"]/text()').re(r'\d{4}')
        if year:
            year = year[0]
        else:
            yield None
            return
        if self.which_year == year:
            passers = response.xpath('//table//tr[count(./td)=4]')
            for passer in passers:
                pil = PasserItemLoader(selector=passer)
                pil.add_xpath('student_number', './td[1]/text()')
                pil.add_xpath('name', './td[2]/text()')
                pil.add_xpath('campus', './td[3]/text()')
                pil.add_xpath('course', './td[4]/text()')
                pil.add_value('source', response.url)
                pil.add_xpath('year', '//font[@size="5"]/text()', re='\d{4}')
                yield pil.load_item()
            next_pages = response.xpath(
                '//a[contains(text(), "Next Page")]/@href'
            ).extract()
            for next_page in next_pages:
                yield Request(urljoin(response.url, next_page))
        elif int(year) > int(self.which_year):
            url = self.URL_RE.search(response.url).group(1)
            yield Request(
                'http://web.archive.org/web/%s0514131655/%s' % (
                    self.which_year, url
                )
            )



class UpcatArchiveOrgPaginatedSpider(Spider):
    name = "upcat_archiveorg_paginated"
    allowed_domains = ["web.archive.org"]
    which_year = None

    def start_requests(self):
        if self.which_year and self.which_year in START_URLS:
            yield Request(START_URLS[self.which_year])
        else:
            for urls in START_URLS.values():
                yield Request(urls)

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
            pil.add_value('year', self.which_year)
            yield pil.load_item()
