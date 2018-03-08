# -*- coding: utf-8 -*-
import string
import sys
import multiprocessing
import threading as thd
import time
import scrapy
# 导入item中结构化数据模板
import AutoHomeDealer.SqlCon
from AutoHomeDealer.items import AutohomedealerItem
reload(sys)
sys.setdefaultencoding('utf8')

class AdhSpider(scrapy.Spider):

    name = 'adh'
    allowed_domains = ['bitauto.com']
    # 初始URL易车
    start_urls = ['http://dealer.bitauto.com/100116410/news_2.html']
    # 初始化汽车之家 PageUlrs="https://dealer.autohome.com.cn/beihai?countyId=0&brandId=0&seriesId=0&factoryId=0&pageIndex=2&kindId=1&orderType=0&isSale=0"
    def start_requests(self):
        ms = AutoHomeDealer.SqlCon.SqlCon(host=".", user="", pwd="", db="")
        sqlstr = "SELECT DealerKey FROM [dbo].[dealerlist] where dealerkey not in (SELECT  DealerKey from [testdb].[dbo].[BitAutoPriceReduction]with(nolock) group by DealerKey)"
        dealer_list = ms.ExecQuery(sqlstr.encode('utf-8'))
        for dealer in dealer_list:
            item = AutohomedealerItem()
            item['dealer'] = dealer[0]
            url = "http://dealer.bitauto.com/" + str(dealer[0]) + "/news_2.html";
            item['companyurl'] = url
            yield scrapy.Request(url, callback=self.parse, meta={'item': item})

       

    # 设置一个空集合
    # url_set = set()
    def parse(self, response):
        #   <div class="markdowns">
        #  <table width="100%" border="0" cellspacing="0" cellpadding="0"><tr><td class="t_l">
        #<a target="_blank" href="/100035376/news/000101/156637781.html">奥迪A8L</a>
        #</td>

        try:
            print 2
            allPics = response.xpath('//div[@class="markdowns"]/table/tr[td]')
            item = response.meta['item']
            for pic in allPics:
                # 分别处理每个图片，取出名称及地址
                # each.xpath("./td[1]/a/@href").extract()[0]
                # <td class="jade">送礼包</td>
                ifpricereduction=pic.xpath('./td[@class="jade"]/text()').extract()[0]
                if '礼包' not  in ifpricereduction:
                    item['newsurl'] = pic.xpath('./td[@class="t_l"]/a[@target="_blank"]/@href').extract()[0]
                # companyurl = pic.xpath('./li[5]/a[@class="link"]/@href').extract()[0]
                # item['companyurl'] = companyurl
                # print item['company'],companyurl
                # 返回爬取信息
                    reductionurl = "http://dealer.bitauto.com" + item['newsurl']
                    yield scrapy.Request(reductionurl, callback=self.parse_item, meta={'item': item})
                # yield生成请求，将新的url加入到爬取队列中，cl为url，callback为新的爬取调用的parse名称，这个项目新定义的为parse_item。

          
        except:
            print response.meta['item']

            

    def parse_item(self, response):
        try:
            #  <div class="art_table"><table width="100%" border="0" cellspacing="0" cellpadding="0">
            #<tr>
            allnews = response.xpath('//div[@class="art_table"]/table/tr[td]')
            # <input type="hidden" id="SeriesId" value="3397" /><input type="hidden" id="SeriesName" value="瑞虎3" />
            # carid = response.xpath('//input[@id="SeriesId"]/@value').extract()[0]
            # carname = response.xpath('//input[@id="SeriesName"]/@value').extract()[0]
            for news in allnews:
                item = response.meta['item']
                item['carstyle'] = news.xpath('./td[6]/a/@data-carid').extract()[0]
                item['carNakedPrice'] = news.xpath('./td[4][@class="imp"]/text()').extract()[0]
                item['carPriceReduction'] = news.xpath('./td[3]/span/text()').extract()[0]
                item['carMSRP'] = news.xpath('./td[2]/text()').extract()[0]
                yield item
        except:
            print response.meta['item']


