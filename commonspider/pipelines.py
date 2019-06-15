# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from commonspider.settings import MYSQL_HOST, MYSQL_PORT, MYSQL_DB, MYSQL_USER, MYSQL_PASSWORD, MYSQL_CHARSET
from pymysql import *
import logging


class CommonspiderPipeline(object):
    def __init__(self):
        self.conn = connect(host=MYSQL_HOST,
                            port=MYSQL_PORT,
                            database=MYSQL_DB,
                            user=MYSQL_USER,
                            password=MYSQL_PASSWORD,
                            charset=MYSQL_CHARSET
                            )
        # 创建游标
        self.cs1 = self.conn.cursor()

    def process_item(self, item, spider):
        try:
            sql = 'INSERT IGNORE into commonspider (url, price, title,product_id) values (%s,%s,%s,%s)'
            self.conn.ping(reconnect=True)  # 若数据库断开连接则重连
            self.cs1.execute(sql, (item['url'], item['price'], item['title'], item['product_id']))
            self.conn.commit()
            logging.debug('insert mysql success')
        except Exception as e:
            logging.debug('插入数据库失败---------------------%s' % e)

        return item

    def close_spider(self, spider):
        # 当爬虫结束,关闭连接
        # 关闭游标
        self.cs1.close()
        # 关闭连接
        self.conn.close()
