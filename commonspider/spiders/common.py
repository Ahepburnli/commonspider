# -*- coding: utf-8 -*-

'''
暂时将url和对应的规则存储在excel中
url price_rule title_rule

'''
import scrapy
import pandas as pd
from commonspider.items import CommonspiderItem
import logging


class CommonSpider(scrapy.Spider):
    name = 'common'
    allowed_domains = ['common.com']

    # start_urls = ['http://common.com/']

    def start_requests(self):
        df = pd.read_excel('/home/hepburn/commonspider/commonspider/rule.xls')
        # 获取url数组
        urls = df['url'].values
        # print(urls)
        # 增加日志信息
        logging.debug(urls)
        # 获取xpath规则
        # try:
        price_rules = df['price_rule'].values
        # print(price_rule)
        logging.debug(price_rules)
        title_rules = df['title_rule'].values
        logging.debug(title_rules)
        product_id_rules = df['product_id'].values
        # print(title_rule)

        try:
            for index, url in enumerate(urls):
                # print(index)
                # 将url和每个规则对应
                price_rule = price_rules[index]
                product_id_rule = product_id_rules[index]
                title_rule = title_rules[index]

                yield scrapy.Request(url, callback=self.parse,
                                     meta={'price_rule': price_rule, 'title_rule': title_rule,
                                           'product_id_rule': product_id_rule},
                                     dont_filter=True)
        except Exception as e:
            logging.debug('xpath错误或没有---%s---%s' % (url, e))

    def parse(self, response):

        try:
            price_rule = response.meta['price_rule']
            title_rule = response.meta['title_rule']
            product_id_rule = response.meta['product_id_rule']

            item = CommonspiderItem()
            item['url'] = response.url

            # 将各个规则传入对应的xpath中解析
            titles = response.xpath(title_rule).extract()
            print(len(titles))
            prices = response.xpath(price_rule).extract()
            print(len(prices))
            product_ids = response.xpath(product_id_rule).extract()
            print(len(product_ids))

            for index, title in enumerate(titles):
                # 去掉标题中带的空格
                title = title.replace('\n', '')
                title = title.strip()
                item['title'] = title
                logging.debug(item['title'])
                # 获取标题列表
                # print(prices)
                # 通过下标对应价格的title
                price = prices[index]
                # 去掉空格
                price = price.replace('\n', '')
                price = price.replace(' ', '')
                item['price'] = price

                product_id = product_ids[index]
                item['product_id'] = product_id

                logging.debug(item['price'])
                yield item
        except Exception as e:
            logging.debug('出现错误---%s---%s' % (response.url, e))
