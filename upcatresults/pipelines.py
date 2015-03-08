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

class StudentNumberPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, PasserItem):
            if 'student_number' in item:
                item['year'] = int(item['student_number'][:4])
                spider.crawler.stats.inc_value('year/%s' % item['year'], 1)
            else:
                spider.crawler.stats.inc_value('student_number/None', 1)
        return item

class DeduperPipeline(object):
    hash_list = []
    def process_item(self, item, spider):
        if isinstance(item, PasserItem):
            passer_hash = '%d-%s' % (
                item['year'], item['name']
            )
            if passer_hash in self.hash_list:
                return None
            else:
                self.hash_list.append(passer_hash)
        return item
