# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import SqlCon
import urllib2
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')

global strs
strs=''
class AutohomedealerPipeline(object):
    def process_item(self, item, spider):
        ms = SqlCon.SqlCon(host=".", user="sa", pwd="1qaz@WSX", db="testdb")
        try:
            print 6
            newsurl=item['newsurl']
            dealer=item['dealer']
            carMSRP=item['carMSRP'].replace(' ', '')
            carPriceReduction=item['carPriceReduction'].replace(' ', '').replace('↓','')
            carNakedPrice= item['carNakedPrice'].replace(' ', '')
            companyurl=item['companyurl']
            carstyle=item['carstyle']

            sqlstr = "INSERT INTO [dbo].[BitAutoPriceReduction]([DealerKey],[CarMSRP],[CarPriceReduction],[CarNakedPrice],[CompanyUrl],[CarStyle]) VALUES ('%s','%s','%s','%s','%s','%s');" % (dealer,carMSRP,carPriceReduction,carNakedPrice,companyurl,carstyle)
            global  strs
            strs=strs+sqlstr.encode('utf-8')
            if(strs.count(';')>=100):
                ms.ExecNonQuery(strs)
                strs='';
        except  Exception, e:
            print str(e),5

        # print   item['carserialid']
        # print  item['carserialname']
        # print  item['carstyle']
        # print  item['carNakedPrice']
        # print item['carPriceReduction']
        # print  item['carMSRP']
