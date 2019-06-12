# -*- coding: utf-8 -*-

'''
假定url和对应的规则在excel中
url price_rule title_rule

'''
import scrapy
import pandas as pd
from commonspider.items import CommonspiderItem
import logging



class CommonSpider(scrapy.Spider):
    name = 'common'
    allowed_domains = ['common.com']
    start_urls = ['http://common.com/']

    def start_requests(self):
        df = pd.read_excel('/home/hepburn/commonspider/commonspider/rule.xls')
        urls = df['url'].values
        # 读取xpath规则
        price_rule = df['price_rule'].values
        title_rule = df['title_rule'].values
        for index, url in enumerate(urls):
            url = url
            price_rule = price_rule[index]

            title_rule = title_rule[index]
            yield scrapy.Request(url, callback=self.parse, meta={'price_rule': price_rule, 'title_rule': title_rule})

    def parse(self, response):
        # price所在的规则
        price_rule = response.meta['price_rule']
        title_rule = response.meta['title_rule']
        item = CommonspiderItem()
        item['url'] = response.url
        try:
            price = response.xpath(price_rule).extract()
            for index, price in enumerate(price):
                item['price'] = price
                logging.debug(item['price'])
                # 获取标题列表
                titles = response.xpath(title_rule).extract()
                # 通过下表对应价格的title
                item['title'] = titles[index]
                logging.debug(item['title'])
                yield item
        except Exception as e:
            logging.debug('出现错误')
