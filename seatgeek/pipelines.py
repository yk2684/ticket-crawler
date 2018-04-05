# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import csv
import datetime
from scrapy import signals
from scrapy.contrib.exporter import CsvItemExporter
from scrapy.exceptions import DropItem

class SeatgeekPipeline(object):
 
    def process_item(self, item, spider):
        if 'New York' not in item['location']:
            raise DropItem("Performances not in New York")
        #item['performance'] = datetime.datetime.strptime(item['performance'],'%Y%m%d%I%p')
        return item