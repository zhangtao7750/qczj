# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import QczjItem
from urllib.parse import urljoin
from copy import deepcopy
class BmwSpider(scrapy.Spider):
    name = 'bmw'
    allowed_domains = ['car.autohome.com.cn']
    start_urls = ['https://car.autohome.com.cn/pic/brand-15-80.html']

    # rules = (
    #     Rule(LinkExtractor(allow=r'https://car.autohome.com.cn/pic/brand-15-.+'), callback='parse_cate',follow=True),
    # )

    def parse(self, response):
        item = QczjItem()
        # item['big_cate']=response.xpath("//div[@class='cartab-title']/h2/text()").get()
        cates=response.xpath("//div[@class='uibox']//li")
        for cate in cates:

            item['cate']=cate.xpath("./div//a/@title").get()
            cate_url=cate.xpath("./div//a/@href").get()
            item['cate_url']="https://car.autohome.com.cn"+cate_url
            yield scrapy.Request(
                item['cate_url'],
                callback=self.parse_detail,
                meta={'item':deepcopy(item)}
            )

    def parse_detail(self,response):
        item=response.meta['item']
        div_list=response.xpath("//div[@class='uibox']")[1:]
        for div in div_list:
            item['cate_part']=div.xpath(".//a/text()")[0].get()
            item['cate_part_url']="https://car.autohome.com.cn"+div.xpath(".//a/@href")[0].get()
            yield scrapy.Request(
                item['cate_part_url'],
                callback=self.parse_image,
                meta={'item':deepcopy(item)}
            )

    def parse_image(self,response):
        item=response.meta['item']
        item['image_urls']=response.xpath("//div[@class='uibox']//img/@src").getall()
        yield item
        next_url=response.xpath("//a[@class='page-item-next']/@href").get()

        if next_url:
            next_url="https://car.autohome.com.cn"+next_url
            yield scrapy.Request(
                next_url,
                callback=self.parse_image,
                meta={'item':deepcopy(item)}
            )



