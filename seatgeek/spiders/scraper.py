import scrapy
import pandas as pd
import json
import datetime
import re
from seatgeek.items import SeatgeekItem

class seatgeekSpider(scrapy.Spider):
    name = "seatgeek_spider"

    def __init__(self, showname='', **kwargs):
        self.start_urls = ['https://seatgeek.com/%s' % showname + "-tickets?page={}".format(i) for i in range (1,35)]
        super().__init__(**kwargs)  # python3

    custom_settings = {
        'DOWNLOAD_DELAY': 3,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 3,
        'HTTPCACHE_ENABLED': True,
        'FEED_EXPORT_FIELDS': ["currentPrice", "listingId", "listingPrice", "quantity", "row", "score", "seatNumbers", "sectionName", "zoneName",
        "eventId", "performance", "datePulled", "vendor"]
    }

    def parse(self, response):
        item = SeatgeekItem()

        for href in response.xpath('//a[@class="event-listing-title"]/@href').extract():
            item['performance'] = re.sub('[^0-9]','', href.split('/')[-3])+'PM'
            item['location'] = href.split('/')[-4]
            item["eventId"] = href.split('/')[-1]

            yield scrapy.Request(
                url = 'https://seatgeek.com/listings?id=' + item['eventId'] + '&aid=11955&client_id=MTY2MnwxMzgzMzIwMTU4',
                callback=self.parse_ticketinv,
                meta={'item': item})
                
    def parse_ticketinv(self, response):
        jsonresponse = json.loads(response.body_as_unicode())
        item = response.meta['item']
        for i in jsonresponse["listings"]:
            item["sectionName"] = i["s"]
            item["zoneName"] = i["s"].split(' ')[0]
            item["currentPrice"] = i["p"]
            item["listingPrice"] = i["p"]
            item["row"] = i["r"]
            item["seatNumbers"] = ""
            item['listingId'] = i["id"]
            item['quantity'] = i["q"]
            item['vendor'] = "SeatGeek"
            item['datePulled'] = datetime.datetime.now()
            item['score'] = 0

            yield item.copy()