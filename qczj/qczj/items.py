# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QczjItem(scrapy.Item):
    # define the fields for your item here like:
    cate_url=scrapy.Field()
    cate = scrapy.Field()
    cate_part=scrapy.Field()
    cate_part_url=scrapy.Field()
    image_urls=scrapy.Field()
    images=scrapy.Field()
