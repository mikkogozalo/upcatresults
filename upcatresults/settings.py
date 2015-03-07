# -*- coding: utf-8 -*-

# Scrapy settings for upcatresults project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'upcatresults'

SPIDER_MODULES = ['upcatresults.spiders']
NEWSPIDER_MODULE = 'upcatresults.spiders'

ITEM_PIPELINES = {
    'upcatresults.pipelines.NamePipeline': 100
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'upcatresults (+http://www.yourdomain.com)'
