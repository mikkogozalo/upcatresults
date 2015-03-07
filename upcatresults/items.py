# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import (
    TakeFirst, MapCompose, Compose, Join
)

from upcatresults.utils import student_number_processor, year_processor


class PasserItem(Item):
    name = Field()
    name_first = Field()
    name_last = Field()
    campus = Field()
    course = Field()
    student_number = Field()
    year = Field()
    notes = Field()
    source = Field()


class PasserItemLoader(ItemLoader):
    default_item_class = PasserItem

    default_output_processor = TakeFirst()
    name_in = MapCompose(unicode, unicode.strip)
    name_first_in = MapCompose(unicode, unicode.strip)
    name_last_in = MapCompose(unicode, unicode.strip)
    campus_in = MapCompose(unicode, unicode.strip, unicode.upper)
    course_in = MapCompose(unicode, unicode.strip)
    student_number_in = MapCompose(
        unicode,
        unicode.strip,
        student_number_processor
    )
    year_in = MapCompose(int, year_processor)
    notes_in = MapCompose(unicode, unicode.strip)
    source_in = MapCompose(unicode, unicode.strip)
