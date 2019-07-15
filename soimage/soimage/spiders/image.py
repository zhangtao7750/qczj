# -*- coding: utf-8 -*-
import scrapy
from ..items import SoimageItem
import json
from  urllib.parse import urlencode
class ImageSpider(scrapy.Spider):
    name = 'image'
    allowed_domains = ['images.so.com']
    start_urls = ['http://images.so.com/']

    def start_requests(self):
        data={'ch':'beauty','listtype':'new'}
        base_url='http://images.so.com/zj?'
        for page in range(1,self.settings.get('MAX_PAGES')+1):
            data['sn']=page*30
            url=base_url+urlencode(data)
            yield scrapy.Request(
                url,
                callback=self.parse,
            )



    def parse(self, response):
        result=json.loads(response.text)
        for image  in result.get('list'):
            item=SoimageItem()
            item['id']=image.get('imageid')
            item['url']=image.get('qhimg_url')
            item['title']=image.get('group_title')
            item['thumb']=image.get('qhimg_thumb_url')
            yield item
