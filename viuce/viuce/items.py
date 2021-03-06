# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

def beneficios_serializer(beneficios):

    return '\n'.join(beneficios)

class Vaga(scrapy.Item):

    cargo = scrapy.Field()
    descricao = scrapy.Field()
    beneficios = scrapy.Field(serializer=beneficios_serializer)
    salario = scrapy.Field()
    cidade = scrapy.Field()
    codigo = scrapy.Field()
    data = scrapy.Field()
    url = scrapy.Field()
