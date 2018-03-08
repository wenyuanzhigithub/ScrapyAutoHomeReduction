# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import scrapy
class AutohomedealerItem(scrapy.Item):
    # define the fields for your item here like:
    newsurl = scrapy.Field()
    dealer = scrapy.Field()
    carMSRP = scrapy.Field()
    carPriceReduction = scrapy.Field()
    carNakedPrice = scrapy.Field()
    companyurl = scrapy.Field()
    carstyle = scrapy.Field()
