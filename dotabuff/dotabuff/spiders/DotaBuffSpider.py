# -*- coding: utf-8 -*-

import scrapy
from dotabuff.items import MatchItem, Hero
import urlparse

MATCHES_XPATH = "//tbody//a[contains(@href, 'matches')]/@href"

NEXT_PAGE_XPATH = '//span[@class="next"]/a[@rel="next"]/@href'

RADIANT_HEROES_NAME_XPATH = '//div[@class="team-results"]/section[@class="radiant"]//tbody//tr[@class=" faction-radiant"]//a[contains(@href,"heroes")]/@href'

RADIANT_HEROES_LEVEL_XPATH = '//div[@class="team-results"]/section[@class="radiant"]//td[@class="cell-centered"][1]/text()'

RADIANT_HEROES_KILL_XPATH = '//div[@class="team-results"]/section[@class="radiant"]//td[@class="cell-centered"][2]/text()'

RADIANT_HEROES_DEATH_XPATH = '//div[@class="team-results"]/section[@class="radiant"]//td[@class="cell-centered"][3]/text()'

RADIANT_HEROES_ASSIST_XPATH = '//div[@class="team-results"]/section[@class="radiant"]//td[@class="cell-centered"][4]/text()'

RADIANT_HEROES_ITEMS_XPATH = '//div[@class="team-results"]/section[@class="radiant"]//tr[@class=" faction-radiant"]//td[16]'

DIRE_HEROES_NAME_XPATH = '//div[@class="team-results"]/section[@class="dire"]//tbody//tr[@class=" faction-dire"]//a[contains(@href,"heroes")]/@href'

DIRE_HEROES_LEVEL_XPATH = '//div[@class="team-results"]/section[@class="dire"]//td[@class="cell-centered"][1]/text()'

DIRE_HEROES_KILL_XPATH = '//div[@class="team-results"]/section[@class="dire"]//td[@class="cell-centered"][2]/text()'

DIRE_HEROES_DEATH_XPATH = '//div[@class="team-results"]/section[@class="dire"]//td[@class="cell-centered"][3]/text()'

DIRE_HEROES_ASSIST_XPATH = '//div[@class="team-results"]/section[@class="dire"]//td[@class="cell-centered"][4]/text()'

DIRE_HEROES_ITEMS_XPATH = '//div[@class="team-results"]/section[@class="dire"]//tr[@class=" faction-dire"]//td[16]'

DIRE_HEROES_ITEMS_XPATH = '//div[@class="team-results"]/section[@class="dire"]//tr[@class=" faction-dire"]//td[16]'

class DotaBuffSpider(scrapy.Spider):

    name = 'DotaBuffSpider'
    start_urls = ['https://www.dotabuff.com/matches?game_mode=captains_mode']

    def parse(self, response):

        for match_url in response.xpath(MATCHES_XPATH).extract():

            # estranho, response.url.join gerando url inesperada... TODO: analisar
            # match_url = response.url.join(match_url)
            match_url = urlparse.urljoin(response.url, match_url)
            yield scrapy.Request(match_url, callback=self.parse_match)

        for next_page_url in response.xpath(NEXT_PAGE_XPATH).extract():

            # mesmo problema com response.url.join
            # next_page_url = response.url.join(next_page_url)
            next_page_url = urlparse.urljoin(response.url, next_page_url)
            yield scrapy.Request(next_page_url)


    def parse_match(self, response):


        match = MatchItem()

        match['match_id'] = response.url.rsplit('/')[-1]

# match result - Radiant

        radiant_heroes_names = [x.rsplit('/')[-1] for x in response.xpath(RADIANT_HEROES_NAME_XPATH).extract()]
        radiant_heroes_levels = response.xpath(RADIANT_HEROES_LEVEL_XPATH).extract()
        radiant_heroes_kills = response.xpath(RADIANT_HEROES_KILL_XPATH).extract()
        radiant_heroes_deaths = response.xpath(RADIANT_HEROES_DEATH_XPATH).extract()
        radiant_heroes_assists = response.xpath(RADIANT_HEROES_ASSIST_XPATH).extract()

        radiant_team = [Hero(name=hero_name, level=hero_level, kill=hero_kill, death=hero_death, assist=hero_assist) for hero_name, hero_level, hero_kill, hero_death, hero_assist in zip(radiant_heroes_names, radiant_heroes_levels, radiant_heroes_kills, radiant_heroes_deaths, radiant_heroes_assists)]

        radiant_team_items = [[y.rsplit('/')[-1] for y in x.xpath('div/a/@href').extract()] for x in response.xpath(RADIANT_HEROES_ITEMS_XPATH)]

        for radiant_hero, hero_items in zip(radiant_team, radiant_team_items):

            radiant_hero['items'] = hero_items

        match['radiant_team'] = radiant_team

# match result - Dire

        dire_heroes_names = [x.rsplit('/')[-1] for x in response.xpath(DIRE_HEROES_NAME_XPATH).extract()]
        dire_heroes_levels = response.xpath(DIRE_HEROES_LEVEL_XPATH).extract()
        dire_heroes_kills = response.xpath(DIRE_HEROES_KILL_XPATH).extract()
        dire_heroes_deaths = response.xpath(DIRE_HEROES_DEATH_XPATH).extract()
        dire_heroes_assists = response.xpath(DIRE_HEROES_ASSIST_XPATH).extract()

        dire_team = [Hero(name=hero_name, level=hero_level, kill=hero_kill, death=hero_death, assist=hero_assist) for hero_name, hero_level, hero_kill, hero_death, hero_assist in zip(dire_heroes_names, dire_heroes_levels, dire_heroes_kills, dire_heroes_deaths, dire_heroes_assists)]

        dire_team_items = [[y.rsplit('/')[-1] for y in x.xpath('div/a/@href').extract()] for x in response.xpath(DIRE_HEROES_ITEMS_XPATH)]

        for dire_hero, hero_items in zip(dire_team, dire_team_items):

            dire_hero['items'] = hero_items

        match['dire_team'] = dire_team

        yield match

