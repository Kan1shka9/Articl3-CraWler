import scrapy
from tutsplustuts.items import TutsplustutsItem
import re
import requests

class MySpider(scrapy.Spider):
    name = "tutspider"
    #allowed_domains = ["*"]
    start_urls  = ["http://tutsplus.com/tutorials"]

    def parse(self, response):
        # Process all article links
        urls = response.xpath('//a[@class="posts__post-title "]/@href').extract()
        for url in urls:
            absolute_url = response.urljoin(url)
            request = scrapy.Request(absolute_url, callback=self.article)
            yield request

        # Process next page
        next_page_url = response.xpath('//a[@class="pagination__button pagination__next-button"]/@href').extract_first()
        absolute_next_page_url = response.urljoin(next_page_url)
        request = scrapy.Request(absolute_next_page_url, callback=self.parse)
        yield request

    def article(self, response):
        title = response.xpath('//h1[@class="content-header__title"]/text()').extract_first()
        author = response.xpath('//a[@class="content-header__author-link"]/text()').extract_first()
        published_date = response.xpath('//time[@class="content-header__publication-date"]/@title').extract_first()
        article_stats = {
            'title': title,
            'author': author,
            'published_date': published_date}
        yield article_stats