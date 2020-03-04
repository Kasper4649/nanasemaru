# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from nanasemaru.items import NanasemaruItem


class NonnoSpider(CrawlSpider):
    name = 'nonno'
    allowed_domains = ['nonno.hpplus.jp']
    start_urls = ['https://nonno.hpplus.jp/word/%E8%A5%BF%E9%87%8E%E4%B8%83%E7%80%AC?page=1&']

    rules = (
        Rule(LinkExtractor(allow=r'.+page=\d+&', restrict_xpaths="//div[@class='pagination']")),
        Rule(LinkExtractor(allow=r'.+article.+', restrict_xpaths="//div[@class='section clearfix']"),
             callback='parse_page'),
    )

    def parse_page(self, response):
        item = NanasemaruItem()
        item['article_id'] = response.url.split("/")[-1]
        item['article_title'] = response.xpath('//h1[@class="content_title"]/text()').get().strip()

        if "半の人気" in item['article_title']:
            return

        item['article_datetime'] = response.xpath('//time[@class="date"]/text()').get().strip()
        item['image_urls'] = response.xpath('//div[@class="article"]//img/@src').getall()
        yield item
