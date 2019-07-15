# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from  scrapy.pipelines.images import ImagesPipeline
from scrapy import Request
from scrapy.exceptions import DropItem
class SoimagePipeline(object):
    def process_item(self, item, spider):
        return item



class MyImagePipeline(ImagesPipeline):
    # def get_media_requests(self, item, info):
    #
    #     yield Request(item['url'])
    # def file_path(self, request, response=None, info=None):
    #     url=Request.url
    #     file_name=url.split('/')[-1]
    #     title=request.meta['item']['title']
    #     path=title+'/'+file_name
    #     return path
    # def item_completed(self, results, item, info):
    #     images_paths=[x['path'] for ok,x in results if ok]
    #     if not images_paths:
    #         raise DropItem('Image Download Failed')
    #     return item
    def get_media_requests(self, item, info):

        yield Request(item['url'],meta={'item':item})


    def file_path(self, request, response=None, info=None):
        url=request.url
        file_name=url.split('/')[-1]
        title=request.meta['item']['title']
        path=title+'/'+file_name
        return path

    def item_completed(self, results, item, info):
        image_path=[x['path'] for ok,x in results if ok]
        if not image_path:
            raise DropItem("Contain No Images")
        return item


class MongoPipeline(object):
    def  __init__(self,mongo_url,mongo_db):
        self.mongo_url=mongo_url
        self.mongo_db=mongo_db

    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            mongo_url=crawler.settings.get('MONGO_URL'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )
    def open_spider(self,spider):
        self.client=pymongo.MongoClient(self.mongo_url)
        self.db=self.client[self.mongo_db]

    def process_item(self,item,spider):
        self.db[spider.name].insert(dict(item))
        return item
    def close_spider(self,spider):
        self.client.close()
