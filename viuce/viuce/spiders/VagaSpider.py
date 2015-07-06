# -*- encoding: utf-8 -*-

import scrapy
from viuce.items import Vaga

class VagaSpider(scrapy.Spider):

    start_urls = ["http://www.ceviu.com.br/buscar/vaga/emprego-444300"]
    name = "VagaSpider"

    def parse(self, response):

        vaga = response.xpath('//div[@class="descricaoVaga"]')[0]
        d_col = vaga.xpath('div[@id="direitaD"]')

        vaga = Vaga()

        vaga['cargo'] = d_col[0].xpath('text()')[0].extract().strip()
        vaga['descricao'] = '\n'.join(x.strip() for x in d_col[1].xpath('text()').extract())
        vaga['beneficios'] = d_col[2].xpath('ul/li/text()').extract()

        print vaga
