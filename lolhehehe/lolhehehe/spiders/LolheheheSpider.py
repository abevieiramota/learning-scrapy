# -*- coding: utf-8 -*-
import scrapy
from lolhehehe.items import LolheheheItem


class LolhehehespiderSpider(scrapy.Spider):

    name = "LolheheheSpider"
    start_urls = (
        'http://lolhehehe.com/category/galeria',
    )

    def parse(self, response):

        for galeria_url in response.xpath('//p/a[contains(@class, "more-link")]/@href').extract():

            yield scrapy.Request(galeria_url, callback=self.parse_galeria)

        for page_url in response.xpath(u'//a[contains(text(), "Próxima página")]/@href').extract():

            yield scrapy.Request(page_url)


    def parse_galeria(self, response):

        img_urls = response.xpath('//p/img/@src').extract()
        img_urls = [img_url.split('?')[0] for img_url in img_urls]

        item = LolheheheItem()
        item['file_urls'] = img_urls

        yield item
