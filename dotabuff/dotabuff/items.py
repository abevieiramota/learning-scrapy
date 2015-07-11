# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class Hero(scrapy.Item):

    name = scrapy.Field()
    level = scrapy.Field()
    kill = scrapy.Field()
    death = scrapy.Field()
    assist = scrapy.Field()
    items = scrapy.Field()

class MatchItem(scrapy.Item):

    match_id = scrapy.Field()
    radiant_team = scrapy.Field()
    dire_team = scrapy.Field()
