# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request
from scrapy.exceptions import DropItem
class QczjPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for url in item['image_urls']:
            url="https:"+url.split('t_')[0]+url.split('t_')[1]
            yield Request(
                url,
                meta={'item':item}
            )
    def file_path(self, request, response=None, info=None):
        url=request.url
        file_name=url.split('/')[-1]
        title1=request.meta['item']['cate']
        title2=request.meta['item']['cate_part']
        path=title1+'/'+title2+'/'+file_name
        return path
    def item_completed(self, results, item, info):
        image_path=[x['path'] for ok,x in results if ok]
        if not image_path:
            raise DropItem('NoImages')
        return item



