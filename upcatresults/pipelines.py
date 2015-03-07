# -*- coding: utf-8 -*-

from scrapy.exceptions import DropItem

from upcatresults.items import PasserItem


class NamePipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, PasserItem):
            if not 'name' in item:
                raise DropItem('No name was extracted')
            if not isinstance(item['name'], basestring):
                return None
            name = item['name'].split(', ')
            if len(name) == 2:
                item['name_first'] = name[1]
                item['name_last'] = name[0]
        return item
