# -*- encoding: utf-8 -*-

import scrapy
from viuce.items import Vaga
import urlparse
import re

PAGE_SIZE = 100
INI_REPLACER = re.compile(r'(?<=&ini=)\d+')

class VagaSpider(scrapy.Spider):

    start_urls = ["http://www.ceviu.com.br/buscar/empregos?itensPagina=%d&ini=0" % PAGE_SIZE]

    name = "VagaSpider"

    map_html_to_attr = {
    'Cargo:': 'cargo',
    u'Descrição:': 'descricao',
    u'Salário:': 'salario',
    'Cidade:': 'cidade',
    u'Benefícios': 'beneficios'}

    map_attr_to_xpath = {
    'cargo': lambda x: x.xpath('text()')[0].extract().strip(),
    'descricao': lambda x: '\n'.join(t.strip() for t in x.xpath('text()').extract()),
    'salario': lambda x: x.xpath('text()')[0].extract().strip(),
    'beneficios': lambda x: x.xpath('ul/li/text()').extract(),
    'cidade': lambda x: x.xpath('text()')[0].extract().strip()}

    def parse(self, response):

        relative_vaga_urls = response.xpath('//div[@id="esquerda"]/span[1]/a/@href').extract()

        if not relative_vaga_urls:

            return

        for relative_vaga_url in relative_vaga_urls:

            vaga_url = urlparse.urljoin(response.url, relative_vaga_url)

            yield scrapy.Request(vaga_url, callback=self.parse_vaga)

        # TODO: melhorar essa gambiarra hehe

        new_ini = int(response.url.rsplit('=')[-1]) + PAGE_SIZE

        new_url = INI_REPLACER.sub(str(new_ini), response.url)

        yield scrapy.Request(new_url)



    def parse_vaga(self, response):

        vaga = response.xpath('//div[@class="descricaoVaga"]')[0]

        e_cols = vaga.xpath('div[@id="esquerdaD"]/strong/text()')
        d_cols = vaga.xpath('div[@id="direitaD"]')

        vaga = Vaga()

        vaga['url'] = response.url
        vaga['codigo'] = response.xpath('//div[@id="direita"]')[0].xpath('span/text()')[0].extract()
        vaga['data'] = response.xpath('//div[@id="direita"]')[0].xpath('text()')[3].extract().strip()

        for e_col, d_col in zip(e_cols, d_cols):

            html_col = e_col.extract().strip()

            if html_col in VagaSpider.map_html_to_attr:

                attr_name = VagaSpider.map_html_to_attr[html_col]
                attr_value = VagaSpider.map_attr_to_xpath[attr_name](d_col)

                vaga[attr_name] = attr_value

        print vaga
